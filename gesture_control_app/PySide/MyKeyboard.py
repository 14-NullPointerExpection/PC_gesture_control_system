from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from GestureAlgorithm.Action.VirtualKeyboard import VirtualKeyboard
import sys
def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


@singleton
class myKeyboard(QWidget):
    def __init__(self):
        super().__init__()
        # # 设置窗口无边框； 设置窗口置顶；
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.keyboard = VirtualKeyboard()

        self.keyboard_image = None
        self.can_destroy = None
        self.image = None

        self.timer = None


    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.keyboard_image)

    def timerEvent(self, event) -> None:

        self.keyboard_image,self.can_destroy = self.keyboard.action(self.image,self.points)

        if self.can_destroy:
            self.hide()
        self.update()

    def action(self,image,points):
        self.image = image
        self.points = points
        if self.timer is not None:
            self.killTimer(self.timer)
        self.timer = self.startTimer(200)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    myKeyboard = myKeyboard()
    myKeyboard.show()
    sys.exit(app.exec_())
