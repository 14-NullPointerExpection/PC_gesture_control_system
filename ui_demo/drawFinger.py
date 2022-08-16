from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import PySide2.QtCore as QtCore
import sys

class MyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # # 设置窗口无边框； 设置窗口置顶；
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        # 设置透明度(0~1)
        self.setWindowOpacity(0.9)
        # 设置鼠标为手状
        self.setCursor(Qt.PointingHandCursor)

        self.startTimer(20)
        self.points = [[-3, 138], [27, 114], [48, 72], [62, 35], [77, 15], [19, 6], [31, -44], [36, -76], [40, -105], [0, 0], [2, -59], [3, -96], [1, -126], [-16, 8], [-25, -44], [-30, -77], [-35, -106], [-31, 27], [-42, -8], [-49, -33], [-54, -58]]
        self.timer = 0

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setPen(QPen(QColor(0, 255, 255), 2, Qt.SolidLine))
        for i in range(4):
            painter.drawLine(self.points[i][0]+300, self.points[i][1]+300, self.points[i+1][0]+300, self.points[i+1][1]+300)

        painter.setPen(QPen(QColor(255, 0, 255), 2, Qt.SolidLine))
        painter.drawLine(self.points[0][0]+300, self.points[0][1]+300, self.points[5][0]+300, self.points[5][1]+300)
        for i in range(5,8):
            painter.drawLine(self.points[i][0]+300, self.points[i][1]+300, self.points[i+1][0]+300, self.points[i+1][1]+300)

        painter.setPen(QPen(QColor(128, 255, 0), 2, Qt.SolidLine))
        # painter.drawLine(self.points[5][0]+300, self.points[5][1]+300, self.points[9][0]+300, self.points[9][1]+300)
        painter.drawLine(self.points[9][0]+300, self.points[9][1]+300, self.points[10][0]+300, self.points[10][1]+300)
        # painter.drawLine(self.points[9][0] + 300, self.points[9][1] + 300, self.points[13][0] + 300,self.points[13][1] + 300)
        # painter.drawLine(self.points[13][0] + 300, self.points[13][1] + 300, self.points[17][0] + 300,self.points[17][1] + 300)
        painter.drawLine(self.points[10][0]+300, self.points[10][1]+300, self.points[11][0]+300, self.points[11][1]+300)
        painter.drawLine(self.points[11][0]+300, self.points[11][1]+300, self.points[12][0]+300, self.points[12][1]+300)

        painter.setPen(QPen(QColor(0,128,255), 2, Qt.SolidLine))

        painter.drawLine(self.points[13][0]+300, self.points[13][1]+300, self.points[14][0]+300, self.points[14][1]+300)
        painter.drawLine(self.points[14][0]+300, self.points[14][1]+300, self.points[15][0]+300, self.points[15][1]+300)
        painter.drawLine(self.points[15][0]+300, self.points[15][1]+300, self.points[16][0]+300, self.points[16][1]+300)

        painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.SolidLine))
        painter.drawLine(self.points[0][0]+300, self.points[0][1]+300, self.points[17][0]+300, self.points[17][1]+300)
        painter.drawLine(self.points[17][0]+300, self.points[17][1]+300, self.points[18][0]+300, self.points[18][1]+300)
        painter.drawLine(self.points[18][0]+300, self.points[18][1]+300, self.points[19][0]+300, self.points[19][1]+300)
        painter.drawLine(self.points[19][0]+300, self.points[19][1]+300, self.points[20][0]+300, self.points[20][1]+300)

        # 设置画笔宽度
        painter.setPen(QPen(QColor(0, 0, 0), 4, Qt.SolidLine))

        # 画圆点
        for i in range(len(self.points)):
            painter.drawPoint(self.points[i][0]+300, self.points[i][1]+300)
    def timerEvent(self, event) -> None:
        if self.timer>10:
            return
        self.timer += 1
        self.update()

if __name__ == '__main__':

    # 设置屏幕自适应
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication([])
    # 获取主显示器分辨率
    screen_width = app.primaryScreen().geometry().width()
    screen_height = app.primaryScreen().geometry().height()

    gui = MyWidget()
    # 设置最初出现的位置
    window_width = 600
    window_height = 600
    gui.setGeometry(screen_width - window_width - 10, screen_height//2 - 150, window_width, window_height)
    # 设置坐标中心点

    gui.show()
    sys.exit(app.exec_())
