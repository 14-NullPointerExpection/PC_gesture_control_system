'''
    @description: This is the main window of the application.
    @Date: 2022-08-15
'''
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys
import os
from PySide.UserConfigWindow import UserConfigWindow
from PySide.SystemConfigWindow import SystemConfigWindow
from PySide.HelpWindow import HelpWindow
from PySide.MyTabWidget import MyTabWidget
from PySide.utils.PropertiesHandler import PropertyHandler
from PySide.utils.MyMessageBox import MyMessageBox
from PySide.utils.MyLoading import MyLoading
from PySide.utils.ThreadUtils import stop_thread
from PySide.GestureFloatingWindow import GestureFloatingWindow
from PySide.ModelFloatingWindow import ModelFloatingWindow
from GestureAlgorithm import camera
from GestureAlgorithm.camera import Camera
import threading
from PySide.MyKeyboard import MyKeyboard

# 设置gesture_control_app文件夹为当前工作目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 设置窗口的大小
FLOATING_WINDOW_WIDTH = 300
FLOATING_WINDOW_HEIGHT = 300

# 获取主显示器分辨率
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._message_box = None
        self._loading = None
        self._status = 0
        self.setWindowTitle('手势识别')
        self.setObjectName('main_window')
        properties = PropertyHandler('settings.properties').get_properties()
        if properties is None:
            self._message_box = MyMessageBox('配置文件打开失败', 'error')
            self.close()

        # 手势控件
        self._camera = None # 相机
        self._camera_thread = None # 相机线程
        self._keyboard = None # 键盘
        self._gesture_window = None # 手势窗体
        self._model_window = None # 模型窗体
        # 其他控件
        self._user_config_window = UserConfigWindow(properties, self)
        self._system_config_window = SystemConfigWindow(properties, self)
        self._help_window = HelpWindow(self)
        self._tabs = MyTabWidget(self)
        self._btn_launch_mousemove = QPushButton(self)
        self._btn_launch_shortcut = QPushButton(self)
        self._btn_stop_launch = QPushButton(self)
        
        self.initUI()
        # 引入样式
        with open('PySide/resources/qss/MainWindow.qss', 'r') as f:
            self.setStyleSheet(f.read())

        self.startTimer(10)

    def center(self):
        size = self.geometry()
        self.move((SCREEN_WIDTH-size.width())//2, (SCREEN_HEIGHT-size.height())//2)

    def initUI(self):
        # 窗体样式
        self.show()
        self.setFixedSize(800, 700)
        self.center()
        # tabs样式
        self._tabs.show()
        self._tabs.setTabPosition(QTabWidget.North) # tab在顶部横向排列
        self._tabs.addTab(self._user_config_window, '用户自定义')
        self._tabs.addTab(self._system_config_window, '系统配置')
        self._tabs.addTab(self._help_window, '帮助')
        self._tabs.setGeometry(QRect(10, 10, 780, 550))
        self._tabs.changeEvent = self.on_tabs_change
        self._tabs.tabBar().setCursor(Qt.PointingHandCursor)
        # 启动按钮样式
        self._btn_launch_mousemove.show()
        self._btn_launch_mousemove.setText('启动鼠标控制')
        self._btn_launch_mousemove.setGeometry(QRect(160, 600, 200, 50))
        self._btn_launch_mousemove.setObjectName('btn_launch')
        self._btn_launch_mousemove.setCursor(QCursor(Qt.PointingHandCursor))
        self._btn_launch_mousemove.clicked.connect(self.on_btn_launch_mousemove_clicked)

        self._btn_launch_shortcut.show()
        self._btn_launch_shortcut.setText('启动快捷手势控制')
        self._btn_launch_shortcut.setGeometry(QRect(420, 600, 200, 50))
        self._btn_launch_shortcut.setObjectName('btn_launch')
        self._btn_launch_shortcut.setCursor(QCursor(Qt.PointingHandCursor))
        self._btn_launch_shortcut.clicked.connect(self.on_btn_launch_shortcut_clicked)

        self._btn_stop_launch.hide()
        self._btn_stop_launch.setText('停止')
        self._btn_stop_launch.setObjectName('btn_launch')
        self._btn_stop_launch.setGeometry(QRect(340, 600, 100, 50))
        self._btn_stop_launch.setCursor(QCursor(Qt.PointingHandCursor))
        self._btn_stop_launch.clicked.connect(self.on_btn_stop_launch_clicked)

    def init_camera_windows_and_thread(self):
        if (self._camera is not None):
            # 相机线程
            self._camera_thread = threading.Thread(target=camera.start, args=(self._camera,))
            self._camera_thread.start()
            # 手势窗体
            self._gesture_window = GestureFloatingWindow(self._camera)
            self._gesture_window.setGeometry(SCREEN_WIDTH - FLOATING_WINDOW_WIDTH - 10, SCREEN_HEIGHT // 2 - 400, FLOATING_WINDOW_WIDTH, FLOATING_WINDOW_HEIGHT+100)
            self._gesture_window.show()
            # 模型窗体
            self._model_window = ModelFloatingWindow(self._camera)
            self._model_window.setGeometry(SCREEN_WIDTH - FLOATING_WINDOW_WIDTH - 10, SCREEN_HEIGHT // 2 + 100, FLOATING_WINDOW_WIDTH, FLOATING_WINDOW_HEIGHT)
            self._model_window.show()
            # 按钮显示状态
            self._btn_launch_mousemove.hide()
            self._btn_launch_shortcut.hide()
            self._btn_stop_launch.show()
    
    def handle_btn_launch_mousemove_click(self):
        self._camera = Camera('models/125.pb', class_names=['1', '2', '5'], mode=camera.MOUSE_CONTROL_MODE)
        self._loading.stop()
        self._status = 1
    
    def handle_btn_launch_shortcut_click(self):
        self._camera = Camera('models/0ulr.pb', class_names=['0', 'u', 'l', 'r'], mode=camera.SHORTCUTS_MODE)
        self._loading.stop()
        self._status = 2

    def on_btn_launch_mousemove_clicked(self):
        self._loading = MyLoading('加载摄像模块中', self)
        threading.Thread(target=self.handle_btn_launch_mousemove_click).start()

    def on_btn_launch_shortcut_clicked(self):
        self._loading = MyLoading('加载摄像模块中', self)
        threading.Thread(target=self.handle_btn_launch_shortcut_click).start()
        
    def on_btn_stop_launch_clicked(self):
        # 终止线程
        stop_thread(self._camera_thread)
        self._camera_thread = None
        self._camera = None
        self._keyboard = None
        self._gesture_window = None
        self._model_window = None
        # 按钮显示状态
        self._btn_launch_mousemove.show()
        self._btn_launch_shortcut.show()
        self._btn_stop_launch.hide()


    def on_tabs_change(self, event):
        pass

    def paintEvent(self, event: QPaintEvent) -> None:
        # 绘制背景图片
        painter = QPainter(self)
        # painter.drawPixmap(self.rect(), QPixmap('PySide/resources/images/bgimage.png'))

    def closeEvent(self, event: QCloseEvent) -> None:
        # 终止线程
        if (self._camera_thread is not None):
            stop_thread(self._camera_thread)
        # 关闭窗体
        event.accept()
    
    def timerEvent(self, event: QTimerEvent) -> None:
        if (self._status == 0):
            return
        if (self._status == 1): # 点击启动鼠标移动按钮
            self.init_camera_windows_and_thread()
            # 键盘
            self._keyboard = MyKeyboard(self._camera)
            self._keyboard.hide()
        if (self._status == 2):
            self.init_camera_windows_and_thread()
        self._status = 0
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_F1:
            if self._camera is not None and self._camera_thread is not None:
                self.on_btn_stop_launch_clicked()
            
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    SCREEN_WIDTH = app.primaryScreen().size().width()
    SCREEN_HEIGHT = app.primaryScreen().size().height()
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())