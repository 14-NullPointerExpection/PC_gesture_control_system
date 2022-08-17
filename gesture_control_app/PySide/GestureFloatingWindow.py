from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import PySide2.QtCore as QtCore
import sys
from FloatingWindow import FloatingWindow

class GestureFloatingWindow(FloatingWindow):
    def __init__(self,camera):
        super().__init__()
        self.camera = camera
        
        self._points = self.camera.points.copy()
        for i in range(len(self._points)):
            self._points[i][0] = self._points[i][0] * 0.75
            self._points[i][1] = self._points[i][1] * 0.75

        self.pred_value = 0

    def paintEvent(self, event):
        painter = QPainter(self)

        # painter.scale(0.75, 0.75)
        # 骨架
        painter.setPen(QPen(QColor(128, 128, 128), 4, Qt.SolidLine))
        painter.drawLine(self._points[0][0] + 100, self._points[0][1] + 100, self._points[5][0] + 100,
                         self._points[5][1] + 100)
        painter.drawLine(self._points[0][0] + 100, self._points[0][1] + 100, self._points[17][0] + 100,
                         self._points[17][1] + 100)
        # 尾指
        painter.setPen(QPen(QColor(128, 128, 0), 4, Qt.SolidLine))
        painter.drawLine(self._points[17][0] + 100, self._points[17][1] + 100, self._points[18][0] + 100,
                         self._points[18][1] + 100)
        painter.drawLine(self._points[18][0] + 100, self._points[18][1] + 100, self._points[19][0] + 100,
                         self._points[19][1] + 100)
        painter.drawLine(self._points[19][0] + 100, self._points[19][1] + 100, self._points[20][0] + 100,
                         self._points[20][1] + 100)

        # 无名指
        painter.setPen(QPen(QColor(0, 128, 128), 4, Qt.SolidLine))

        painter.drawLine(self._points[13][0] + 100, self._points[13][1] + 100, self._points[14][0] + 100,
                         self._points[14][1] + 100)
        painter.drawLine(self._points[14][0] + 100, self._points[14][1] + 100, self._points[15][0] + 100,
                         self._points[15][1] + 100)
        painter.drawLine(self._points[15][0] + 100, self._points[15][1] + 100, self._points[16][0] + 100,
                         self._points[16][1] + 100)

        # 中指
        painter.setPen(QPen(QColor(128, 0, 128), 4, Qt.SolidLine))
        painter.drawLine(self._points[9][0] + 100, self._points[9][1] + 100, self._points[10][0] + 100,
                         self._points[10][1] + 100)
        painter.drawLine(self._points[10][0] + 100, self._points[10][1] + 100, self._points[11][0] + 100,
                         self._points[11][1] + 100)
        painter.drawLine(self._points[11][0] + 100, self._points[11][1] + 100, self._points[12][0] + 100,
                         self._points[12][1] + 100)

        # 食指
        painter.setPen(QPen(QColor(255, 0, 0), 4, Qt.SolidLine))
        for i in range(5, 8):
            painter.drawLine(self._points[i][0] + 100, self._points[i][1] + 100, self._points[i + 1][0] + 100,
                             self._points[i + 1][1] + 100)

        painter.setPen(QPen(QColor(0, 255, 0), 4, Qt.SolidLine))
        # 拇指
        for i in range(4):
            painter.drawLine(self._points[i][0] + 100, self._points[i][1] + 100, self._points[i + 1][0] + 100, self._points[i + 1][1] + 100)

        # # 分割线
        painter.setPen(QPen(QColor(0, 0, 0), 3, Qt.SolidLine))
        painter.drawLine(0, 200, self._screen_width, 200)

        # 设置字体大小
        painter.setFont(QFont('微软雅黑', 13))
        painter.drawText(25,235,'当前预测值 : '+ str(self.pred_value))

    def timerEvent(self, event) -> None:
        self._points = self.camera.points.copy()
        for i in range(len(self._points)):
            self._points[i][0] = self._points[i][0] * 0.75
            self._points[i][1] = self._points[i][1] * 0.75
        self.update()



if __name__ == '__main__':

    # 设置屏幕自适应
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication([])
    # 获取主显示器分辨率
    screen_width = app.primaryScreen().geometry().width()
    screen_height = app.primaryScreen().geometry().height()

    gui = GestureFloatingWindow()
    # 设置最初出现的位置
    window_width = 200
    window_height = 250
    gui.setGeometry(screen_width - window_width - 10, screen_height//2 - 300, window_width, window_height)
    # 设置坐标中心点

    gui.show()
    sys.exit(app.exec_())
