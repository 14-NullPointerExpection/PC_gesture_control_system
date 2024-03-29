"""
author: XP
desc: 展示当前模式的悬浮窗
"""
import _thread
import sys

import pyautogui as pag
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from PySide.FloatingWindow import FloatingWindow
from GestureAlgorithm import camera
from GestureAlgorithm.camera import Camera

# 设置窗口大小
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 300

# 模式悬浮窗类，用以显示当前模式
class ModelFloatingWindow(FloatingWindow):
    def __init__(self, camera):
        super().__init__()
        # super(ModelFloatingWindow, self).__init__(parent)
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.camera = camera
        self.startTimer(10)

    def paintEvent(self, event):
        painter = QPainter(self)
        # 设置画笔颜色
        painter.setPen(QPen(QColor(0, 0, 0), 3, Qt.SolidLine))
        # 设置字体大小
        painter.setFont(QFont('微软雅黑', 11))
        # 绘制文字
        if self.camera.mode == 0:
            self.resize(300, 200)
            if self.camera.mouse_status == 0:
                painter.drawText(10, 50, '当前模式 : 鼠标操控')
                painter.drawText(10, 150, '鼠标位置 : ' + str(pag.position().x) + ',' + str(pag.position().y))
                if not self.camera.mouse_moving._can_action:
                    painter.drawText(10, 100, '当前事件 : 鼠标点击')
                else:
                    painter.drawText(10, 100, '当前事件 : 无')
            elif self.camera.mouse_status == 1:
                painter.drawText(10, 50, '当前模式 : 屏幕滚动')
                if not self.camera.scroll_screen._can_action:
                    painter.drawText(10, 100, '当前事件 : 屏幕滚动')
                else:
                    painter.drawText(10, 100, '当前事件 : 无')
        elif self.camera.mode == 1:
            self.resize(300, 100)
            painter.drawText(30, 50, '当前模式 : 快捷指令')
            # painter.drawText(10, 100, '当前事件 : ' + self._click_event)

    def timerEvent(self, event) -> None:
        self.update()


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
    gui.setGeometry(screen_width - WINDOW_WIDTH - 10, screen_height // 2 + 100, WINDOW_WIDTH, WINDOW_HEIGHT)
    # 设置坐标中心点
    gui.show()
    sys.exit(app.exec_())
