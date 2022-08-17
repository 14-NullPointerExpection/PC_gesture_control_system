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

# 设置PySide文件夹为当前工作目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('手势识别')
        # 引入样式
        with open('resources/qss/MainWindow.qss', 'r') as f:
            self.setStyleSheet(f.read())

        self._user_config_window = UserConfigWindow(self)
        self._system_config_window = SystemConfigWindow(self)
        self._tabs = QTabWidget(self)
        self.initUI()

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())//2, (screen.height()-size.height())//2)

    def initUI(self):
        # 窗体样式
        self.show()
        self.resize(800, 600)
        self.center()
        # tabs样式
        self._tabs.show()
        self._tabs.setTabPosition(QTabWidget.North) # tab在顶部横向排列
        self._tabs.addTab(self._user_config_window, '用户自定义')
        self._tabs.addTab(self._system_config_window, '系统配置')
        self._tabs.setGeometry(QRect(10, 10, 750, 550))






if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())