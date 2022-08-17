import sys

from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from FloatingWindow import FloatingWindow
class ModelFloatingWindow(FloatingWindow):
    def __init__(self,):
        super().__init__()
        # super(ModelFloatingWindow, self).__init__(parent)
        self.WINDOW_WIDTH = 200
        self.WINDOW_HEIGHT = 200
        self._model = '鼠标操控'
        self._click_event = '无'

    def paintEvent(self, event):
        painter = QPainter(self)
        # 设置画笔颜色
        painter.setPen(QPen(QColor(0, 0, 0), 3, Qt.SolidLine))
        # painter.setpen(QPen(Qt.red, 2, Qt.SolidLine))
        # 设置字体大小
        painter.setFont(QFont('微软雅黑', 12))

        # 绘制文字
        painter.drawText(10, 50,'当前模式 : ' + self._model)

        painter.drawText(10, 100,'当前事件 : ' + self._click_event)

        if(self._model == '鼠标操控'):
            painter.drawText(10,150,'鼠标位置 : '+str(self.pos().x())+','+str(self.pos().y()))


if __name__ == '__main__':
    # 设置屏幕自适应
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication([])
    # 获取主显示器分辨率
    screen_width = app.primaryScreen().geometry().width()
    screen_height = app.primaryScreen().geometry().height()

    gui = ModelFloatingWindow()
    # 设置最初出现的位置
    window_width = 200
    window_height = 200
    gui.setGeometry(screen_width - window_width - 10, screen_height // 2, window_width, window_height)
    # 设置坐标中心点

    gui.show()
    sys.exit(app.exec_())
