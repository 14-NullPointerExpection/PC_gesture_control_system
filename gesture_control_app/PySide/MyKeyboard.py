"""
author: XP
desc: 展示虚拟键盘
"""
import pyautogui
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from GestureAlgorithm.camera import *


class MyKeyboard(QWidget):
    def __init__(self, cam):
        super().__init__()
        # # 设置窗口无边框； 设置窗口置顶；
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        # 设置10毫秒刷新一次
        self.timer = self.startTimer(10)
        # camera传来的像素点构成的图片
        self.keyboard_image = None
        # 适配屏幕
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = pyautogui.size()
        # camera对象
        self.cam = cam

    def paintEvent(self, event):
        if self.cam.mouse_status == 2:

            painter = QPainter(self)
            # painter.scale(0.5, 0.5)
            keyboard_image = self.cam.keyboard_image
            if keyboard_image is not None:
                # 绘图1280*720
                height, width, channel = keyboard_image.shape
                bytes_per_line = 3 * width
                # 将image转化从QImage
                q_image = QImage(keyboard_image.data, width, height, bytes_per_line, QImage.Format_BGR888)
                self.setGeometry((self.SCREEN_WIDTH - self.width()) / 2, (self.SCREEN_HEIGHT - self.height()) * 0.85,
                                 width, height)
                painter.drawImage(0, 0, q_image)

    def timerEvent(self, event) -> None:
        # 如果当前状态不是键盘，隐藏窗口
        if self.cam.mouse_status != VIRTUAL_KEYBOARD:
            self.hide()
        else:
            self.show()

        self.update()
