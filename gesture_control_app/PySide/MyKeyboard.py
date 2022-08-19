from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import pyautogui
import sys


class MyKeyboard(QWidget):
    def __init__(self):
        super().__init__()
        # # 设置窗口无边框； 设置窗口置顶；
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        # self.keyboard = VirtualKeyboard()
        self.timer = self.startTimer(10)

        self.keyboard_image = None
        self.can_destroy = False
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = pyautogui.size()

    def paintEvent(self, event):

        height, width, channel = self.keyboard_image.shape
        bytesPerline = 3 * width
        qimage = QImage(self.keyboard_image.data, width, height, bytesPerline, QImage.Format_BGR888)

        painter = QPainter(self)

        if self.keyboard_image is not None:
            # 绘图1280*720
            self.setGeometry((self.SCREEN_WIDTH - width) / 2, (self.SCREEN_HEIGHT - height) * 0.85, width, height)
            painter.drawImage(0, 0, qimage)

    def timerEvent(self, event) -> None:

        if self.can_destroy:
            self.hide()
            self.can_destroy = False
        self.update()

    # def action(self, image, points):
    #     self.image = image
    #     self.points = points
    #     self.keyboard_image, self.can_destroy = self.keyboard.action(self.image, self.points)
    #     if self.timer is not None:
    #         self.killTimer(self.timer)
    #
    #     return self.can_destroy


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myKeyboard = MyKeyboard()
    myKeyboard.show()
    sys.exit(app.exec_())
