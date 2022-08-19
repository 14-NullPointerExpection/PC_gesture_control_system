from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import pyautogui
import sys


class MyKeyboard(QWidget):
    def __init__(self,cam):
        super().__init__()
        # # 设置窗口无边框； 设置窗口置顶；
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.timer = self.startTimer(10)

        self.keyboard_image = None
        self.can_destroy = False
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = pyautogui.size()
        self.cam = cam


    def paintEvent(self, event):
        if self.cam.mouse_status == 2:

            painter = QPainter(self)
            # painter.scale(0.5, 0.5)
            keyboard_image = self.cam.keyboard_image
            if keyboard_image is not None:
                # 绘图1280*720
                height, width, channel = keyboard_image.shape
                bytesPerline = 3 * width
                qimage = QImage(keyboard_image.data, width, height, bytesPerline, QImage.Format_BGR888)
                print('----',qimage.width(),qimage.height())
                print(width,height)
                self.setGeometry((self.SCREEN_WIDTH - self.width()) / 2, (self.SCREEN_HEIGHT - self.height()) * 0.85, width, height)
                #self.setGeometry(0,0, width, height)
                #
                painter.drawImage(0, 0, qimage)


    def timerEvent(self, event) -> None:

        if self.cam.mouse_status != 2:
            self.hide()
        else:
            self.show()

        self.update()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    myKeyboard = MyKeyboard()
    myKeyboard.show()
    sys.exit(app.exec_())
