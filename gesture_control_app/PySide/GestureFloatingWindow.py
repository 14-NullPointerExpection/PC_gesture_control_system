"""
author: XP
desc: 展示手掌骨架图及手势预测值的悬浮窗
"""
import sys
import time

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from PySide.FloatingWindow import FloatingWindow
from GestureAlgorithm import camera
from GestureAlgorithm.camera import Camera
from PySide.MyKeyboard import MyKeyboard

# 设置窗口的大小
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 400


class CameraThread(QThread):
    def __init__(self, cam, ):
        super().__init__()
        self.cam = cam

    def run(self):
        camera.start(self.cam)

    # 终止线程
    def stop(self):
        self
        self.quit()
        self.wait()


# 手势悬浮窗类，用以显示手势悬浮窗
class GestureFloatingWindow(FloatingWindow):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera
        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT

        self._points = self.camera.points.copy()
        if len(self._points):
            for i in range(len(self._points)):
                self._points[i] = (self._points[i][0] * 0.75, self._points[i][1] * 0.75)

    def paintEvent(self, event):
        painter = QPainter(self)
        if not self._points:
            painter.setFont(QFont('微软雅黑', 20))
            painter.drawText(50, 175, '未检测到手部')
            return

        # 骨架
        painter.setPen(QPen(QColor(128, 128, 128), 4, Qt.SolidLine))

        painter.drawLine(self._points[0][0] * WINDOW_WIDTH, self._points[0][1] * WINDOW_WIDTH,
                         self._points[5][0] * WINDOW_WIDTH,
                         self._points[5][1] * WINDOW_WIDTH)
        painter.drawLine(self._points[0][0] * WINDOW_WIDTH, self._points[0][1] * WINDOW_WIDTH,
                         self._points[17][0] * WINDOW_WIDTH,
                         self._points[17][1] * WINDOW_WIDTH)
        # 尾指
        painter.setPen(QPen(QColor(128, 128, 0), 4, Qt.SolidLine))
        for i in range(17, 20):
            painter.drawLine(self._points[i][0] * WINDOW_WIDTH, self._points[i][1] * WINDOW_WIDTH,
                             self._points[i + 1][0] * WINDOW_WIDTH,
                             self._points[i + 1][1] * WINDOW_WIDTH)

        # 无名指
        painter.setPen(QPen(QColor(0, 128, 128), 4, Qt.SolidLine))
        for i in range(13, 16):
            painter.drawLine(self._points[i][0] * WINDOW_WIDTH, self._points[i][1] * WINDOW_WIDTH,
                             self._points[i + 1][0] * WINDOW_WIDTH,
                             self._points[i + 1][1] * WINDOW_WIDTH)

        # 中指
        painter.setPen(QPen(QColor(128, 0, 128), 4, Qt.SolidLine))
        for i in range(9, 12):
            painter.drawLine(self._points[i][0] * WINDOW_WIDTH, self._points[i][1] * WINDOW_WIDTH,
                             self._points[i + 1][0] * WINDOW_WIDTH,
                             self._points[i + 1][1] * WINDOW_WIDTH)

        # 食指
        painter.setPen(QPen(QColor(255, 0, 0), 4, Qt.SolidLine))
        for i in range(5, 8):
            painter.drawLine(self._points[i][0] * WINDOW_WIDTH, self._points[i][1] * WINDOW_WIDTH,
                             self._points[i + 1][0] * WINDOW_WIDTH,
                             self._points[i + 1][1] * WINDOW_WIDTH)

        # 拇指
        painter.setPen(QPen(QColor(0, 255, 0), 4, Qt.SolidLine))
        for i in range(4):
            painter.drawLine(self._points[i][0] * WINDOW_WIDTH, self._points[i][1] * WINDOW_WIDTH,
                             self._points[i + 1][0] * WINDOW_WIDTH,
                             self._points[i + 1][1] * WINDOW_WIDTH)

        # # 分割线
        painter.setPen(QPen(QColor(0, 0, 0), 3, Qt.SolidLine))
        painter.drawLine(0, 300, self._screen_width, 300)

        # 设置字体大小
        painter.setFont(QFont('微软雅黑', 13))
        painter.drawText(25, 350, '当前预测值 : ' + str(self.camera.predicted_value))

    # 定时刷新悬浮窗内容
    def timerEvent(self, event) -> None:
        self._points = self.camera.points.copy()
        if not len(self._points):
            self.update()
            return
        for i in range(len(self._points)):
            self._points[i] = (self._points[i][0] * 0.75, self._points[i][1] * 0.75)
        self.update()


if __name__ == '__main__':
    # 设置屏幕自适应
    # QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)

    app = QApplication()
    # 获取主显示器分辨率
    SCREEN_WIDTH = app.primaryScreen().geometry().width()
    SCREEN_HEIGHT = app.primaryScreen().geometry().height()

    c = Camera('../125.pb', class_names=('1', '2', '5'), mode=camera.MOUSE_CONTROL_MODE)
    camera_thread = CameraThread(c)
    camera_thread.start()
    time.sleep(1)
    gui = GestureFloatingWindow(c)
    m = MyKeyboard(c)
    m.hide()
    gui.setGeometry(SCREEN_WIDTH - WINDOW_WIDTH - 10, SCREEN_HEIGHT // 2 - 400, WINDOW_WIDTH, WINDOW_HEIGHT)
    # 设置坐标中心点

    gui.show()
    sys.exit(app.exec_())
