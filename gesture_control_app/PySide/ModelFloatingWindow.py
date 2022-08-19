"""
author: XP
desc: 展示当前模式的悬浮窗
"""
import sys
from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from FloatingWindow import FloatingWindow
from GestureAlgorithm.camera import Camera
from GestureAlgorithm import camera
import pyautogui as pag
import _thread


class ModelFloatingWindow(FloatingWindow):
    def __init__(self, camera):
        super().__init__()
        # super(ModelFloatingWindow, self).__init__(parent)
        self.WINDOW_WIDTH = 300
        self.WINDOW_HEIGHT = 300
        self.camera = camera

    def paintEvent(self, event):
        painter = QPainter(self)
        # 设置画笔颜色
        painter.setPen(QPen(QColor(0, 0, 0), 3, Qt.SolidLine))
        # painter.setpen(QPen(Qt.red, 2, Qt.SolidLine))
        # 设置字体大小
        painter.setFont(QFont('微软雅黑', 11))
        # 绘制文字
        if self.camera.mode == 0:
            painter.drawText(10, 50, '当前模式 : 鼠标操控')
            painter.drawText(10, 100, '当前事件 : ')
            painter.drawText(10, 150, '鼠标位置 : ' + str(pag.position().x) + ',' + str(pag.position().y))
        elif self.camera.mode == 1:
            painter.drawText(10, 50, '当前模式 : 屏幕滚动')
            painter.drawText(10, 100, '当前事件 : ' + self._click_event)


if __name__ == '__main__':
    # 设置屏幕自适应
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication([])
    # 获取主显示器分辨率
    screen_width = app.primaryScreen().geometry().width()
    screen_height = app.primaryScreen().geometry().height()
    c = Camera('../125.pb', class_names=['1', '2', '5'], mode=camera.MOUSE_CONTROL_MODE)
    _thread.start_new_thread(camera.start, (c,))
    gui = ModelFloatingWindow(c)
    # 设置最初出现的位置
    window_width = 300
    window_height = 300
    gui.setGeometry(screen_width - window_width - 10, screen_height // 2+100, window_width, window_height)
    # 设置坐标中心点
    gui.show()
    sys.exit(app.exec_())
