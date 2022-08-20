"""
    @description: This is the main window of the application.
    @Date: 2022-08-15
"""
import os
import sys
import threading

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from GestureAlgorithm import camera
from GestureAlgorithm.camera import Camera
from GestureFloatingWindow import GestureFloatingWindow
from ModelFloatingWindow import ModelFloatingWindow
from PySide.MyKeyboard import MyKeyboard
from components.SystemConfigWindow import SystemConfigWindow
from components.UserConfigWindow import UserConfigWindow
from utils.MyMessageBox import MyMessageBox
from utils.PropertiesHandler import PropertyHandler

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

        # 变量
        self._is_launch = False
        # 相机
        self._camara = Camera('125.pb', class_names=['1', '2', '5'], mode=camera.MOUSE_CONTROL_MODE)
        self._camara_thread = None
        # 键盘
        self._keyboard = MyKeyboard(self._camara)
        self._keyboard.hide()
        # 手势窗体
        self._gesture_window = GestureFloatingWindow(self._camara)
        self._gesture_window.setGeometry(SCREEN_WIDTH - FLOATING_WINDOW_WIDTH - 10, SCREEN_HEIGHT // 2 - 400,
                                         FLOATING_WINDOW_WIDTH, FLOATING_WINDOW_HEIGHT + 100)
        self._gesture_window.show()
        # 模型窗体
        self._model_window = ModelFloatingWindow(self._camara)
        self._model_window.setGeometry(SCREEN_WIDTH - FLOATING_WINDOW_WIDTH - 10, SCREEN_HEIGHT // 2 + 100,
                                       FLOATING_WINDOW_WIDTH, FLOATING_WINDOW_HEIGHT)
        self._model_window.show()
        # 其他控件
        self._user_config_window = UserConfigWindow(self)
        self._system_config_window = SystemConfigWindow(properties, self)
        self._tabs = QTabWidget(self)
        self._btn_launch = QPushButton(self)
        self._btn_launch.clicked.connect(self.launch)
        self.initUI()
        # 引入样式
        with open('PySide/resources/qss/MainWindow.qss', 'r') as f:
            self.setStyleSheet(f.read())

    def center(self):
        size = self.geometry()
        self.move((SCREEN_WIDTH - size.width()) // 2, (SCREEN_HEIGHT - size.height()) // 2)

    def initUI(self):
        # 窗体样式
        self.show()
        self.resize(800, 700)
        self.center()
        # tabs样式
        self._tabs.show()
        self._tabs.setTabPosition(QTabWidget.North)  # tab在顶部横向排列
        self._tabs.addTab(self._user_config_window, '用户自定义')
        self._tabs.addTab(self._system_config_window, '系统配置')
        self._tabs.setGeometry(QRect(10, 10, 750, 550))
        self._tabs.changeEvent = self.on_tabs_change
        # 启动按钮样式
        self._btn_launch.show()
        self._btn_launch.setText('启动')
        self._btn_launch.setObjectName('btn_launch')
        self._btn_launch.setGeometry(QRect(340, 600, 100, 50))
        self._btn_launch.setCursor(QCursor(Qt.PointingHandCursor))

    def launch(self):
        self._is_launch = not self._is_launch
        if self._is_launch:
            if (self._camara is None):
                self._camara = Camera('125.pb', class_names=['1', '2', '5'], mode=camera.MOUSE_CONTROL_MODE)
            self._camara_thread = threading.Thread(target=camera.start, args=(self._camara,))
            self._camara_thread.start()
            self._btn_launch.setText('停止')
        else:
            # 终止线程
            stop_thread(self._camara_thread)
            self._camara_thread = None
            self._camara.mouse_status = 1
            self._btn_launch.setText('启动')

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
