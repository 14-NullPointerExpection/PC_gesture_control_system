'''
    @description: This is the main window of the application.
    @Date: 2022-08-15
'''
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys
import os
from components.UserConfigWindow import UserConfigWindow
from components.SystemConfigWindow import SystemConfigWindow
from utils.PropertiesHandler import PropertyHandler
from utils.MyMessageBox import MyMessageBox
from GestureFloatingWindow import GestureFloatingWindow
from ModelFloatingWindow import ModelFloatingWindow
from GestureAlgorithm import camera
from GestureAlgorithm.camera import Camera
import threading
from PySide.MyKeyboard import MyKeyboard

# 设置PySide文件夹为当前工作目录
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))


# 设置窗口的大小
FLOATING_WINDOW_WIDTH = 300
FLOATING_WINDOW_HEIGHT = 300

# 获取主显示器分辨率
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

import inspect
import ctypes

# 以抛出异常的方式终止线程
def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self._message_box = None
        self.setWindowTitle('手势识别')
        properties = PropertyHandler('settings.properties').get_properties()
        if properties is None:
            self._message_box = MyMessageBox('配置文件打开失败', 'error')
            self.close()

        # 手势控件
        self._camara = None # 相机
        self._camara_thread = None # 相机线程
        self._keyboard = None # 键盘
        self._gesture_window = None # 手势窗体
        self._model_window = None # 模型窗体
        # 其他控件
        self._user_config_window = UserConfigWindow(self)
        self._system_config_window = SystemConfigWindow(properties, self)
        self._tabs = QTabWidget(self)
        self._btn_launch_mousemove = QPushButton(self)
        self._btn_launch_shortcut = QPushButton(self)
        self._btn_stop_launch = QPushButton(self)
        
        self.initUI()
        # 引入样式
        with open('PySide/resources/qss/MainWindow.qss', 'r') as f:
            self.setStyleSheet(f.read())

    def center(self):
        size = self.geometry()
        self.move((SCREEN_WIDTH-size.width())//2, (SCREEN_HEIGHT-size.height())//2)

    def initUI(self):
        # 窗体样式
        self.show()
        self.resize(800, 700)
        self.center()
        # tabs样式
        self._tabs.show()
        self._tabs.setTabPosition(QTabWidget.North) # tab在顶部横向排列
        self._tabs.addTab(self._user_config_window, '用户自定义')
        self._tabs.addTab(self._system_config_window, '系统配置')
        self._tabs.setGeometry(QRect(10, 10, 750, 550))
        self._tabs.changeEvent = self.on_tabs_change
        # 启动按钮样式
        self._btn_launch_mousemove.show()
        self._btn_launch_mousemove.setText('启动鼠标控制')
        self._btn_launch_mousemove.setGeometry(QRect(160, 600, 200, 50))
        self._btn_launch_mousemove.setObjectName('btn_launch')
        self._btn_launch_mousemove.setCursor(QCursor(Qt.PointingHandCursor))
        self._btn_launch_mousemove.clicked.connect(self.on_btn_launch_mousemove_clicked)

        self._btn_launch_shortcut.show()
        self._btn_launch_shortcut.setText('启动快捷键控制')
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

    def init_camara_windows_and_thread(self):
        if (self._camara is not None):
            # 相机线程
            self._camara_thread = threading.Thread(target=camera.start, args=(self._camara,))
            self._camara_thread.start()
            # 手势窗体
            self._gesture_window = GestureFloatingWindow(self._camara)
            self._gesture_window.setGeometry(SCREEN_WIDTH - FLOATING_WINDOW_WIDTH - 10, SCREEN_HEIGHT // 2 - 400, FLOATING_WINDOW_WIDTH, FLOATING_WINDOW_HEIGHT+100)
            self._gesture_window.show()
            # 模型窗体
            self._model_window = ModelFloatingWindow(self._camara)
            self._model_window.setGeometry(SCREEN_WIDTH - FLOATING_WINDOW_WIDTH - 10, SCREEN_HEIGHT // 2 + 100, FLOATING_WINDOW_WIDTH, FLOATING_WINDOW_HEIGHT)
            self._model_window.show()
            # 按钮显示状态
            self._btn_launch_mousemove.hide()
            self._btn_launch_shortcut.hide()
            self._btn_stop_launch.show()

    def on_btn_launch_mousemove_clicked(self):
        # 相机
        self._camara = Camera('125.pb', class_names=['1', '2', '5'], mode=camera.MOUSE_CONTROL_MODE)
        # 相机线程和窗体
        self.init_camara_windows_and_thread()
        # 键盘
        self._keyboard = MyKeyboard(self._camara)
        self._keyboard.hide()

    def on_btn_launch_shortcut_clicked(self):
        # 相机
        self._camara = Camera('0ulr.pb', class_names=['0', 'u', 'l', 'r'], mode=camera.SHORTCUTS_MODE)
        # 相机线程和窗体
        self.init_camara_windows_and_thread()
        
    def on_btn_stop_launch_clicked(self):
        # 终止线程
        stop_thread(self._camara_thread)
        self._camara_thread = None
        self._camara = None
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
        painter.drawPixmap(self.rect(), QPixmap('PySide/resources/images/bgimage.png'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    SCREEN_WIDTH = app.primaryScreen().size().width()
    SCREEN_HEIGHT = app.primaryScreen().size().height()
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())