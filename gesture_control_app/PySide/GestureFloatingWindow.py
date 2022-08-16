from PySide2 import QtWidgets
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import PySide2.QtCore as QtCore
import sys
import test

class GestureFloatingWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # # 设置窗口无边框； 设置窗口置顶；
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        # 设置透明度(0~1)
        self.setWindowOpacity(0.5)
        # 设置鼠标为手状
        self.setCursor(Qt.PointingHandCursor)
        # self.timer = 0
        self._startPos = None
        self._wmGap = None
        self.hidden = False
        dsk = QApplication.primaryScreen()
        self.screen_width = dsk.geometry().width()
        self.screen_height = dsk.geometry().height()
        self.window_width = 200
        self.window_height = 250

        # self.test = test.myThread()
        # self.test.start()

        self.startTimer(100)
        self.points = [[6, 187], [29, 142], [27, 82], [-2, 43], [-30, 18], [28, 0], [36, -77], [39, -125], [39, -167], [0, 0], [-15, -78], [-28, -127], [-40, -169], [-21, 21], [-35, -10], [-22, 33], [-13, 65], [-37, 53], [-46, 26], [-35, 52], [-24, 74]]
        # self.points = self.points*0.75
        for i in range(len(self.points)):
            self.points[i][0] = self.points[i][0]*0.75
            self.points[i][1] = self.points[i][1]*0.75

        self.pred_value = 0

    def paintEvent(self, event):
        painter = QPainter(self)

        # painter.scale(0.75, 0.75)、
        # 骨架
        painter.setPen(QPen(QColor(128, 128, 128), 4, Qt.SolidLine))
        painter.drawLine(self.points[0][0] + 100, self.points[0][1] + 100, self.points[5][0] + 100,
                         self.points[5][1] + 100)
        painter.drawLine(self.points[0][0] + 100, self.points[0][1] + 100, self.points[17][0] + 100,
                         self.points[17][1] + 100)
        # 尾指
        painter.setPen(QPen(QColor(128, 128, 0), 4, Qt.SolidLine))
        painter.drawLine(self.points[17][0] + 100, self.points[17][1] + 100, self.points[18][0] + 100,
                         self.points[18][1] + 100)
        painter.drawLine(self.points[18][0] + 100, self.points[18][1] + 100, self.points[19][0] + 100,
                         self.points[19][1] + 100)
        painter.drawLine(self.points[19][0] + 100, self.points[19][1] + 100, self.points[20][0] + 100,
                         self.points[20][1] + 100)

        # 无名指
        painter.setPen(QPen(QColor(0, 128, 128), 4, Qt.SolidLine))

        painter.drawLine(self.points[13][0] + 100, self.points[13][1] + 100, self.points[14][0] + 100,
                         self.points[14][1] + 100)
        painter.drawLine(self.points[14][0] + 100, self.points[14][1] + 100, self.points[15][0] + 100,
                         self.points[15][1] + 100)
        painter.drawLine(self.points[15][0] + 100, self.points[15][1] + 100, self.points[16][0] + 100,
                         self.points[16][1] + 100)

        # 中指
        painter.setPen(QPen(QColor(128, 0, 128), 4, Qt.SolidLine))
        painter.drawLine(self.points[9][0] + 100, self.points[9][1] + 100, self.points[10][0] + 100,
                         self.points[10][1] + 100)
        painter.drawLine(self.points[10][0] + 100, self.points[10][1] + 100, self.points[11][0] + 100,
                         self.points[11][1] + 100)
        painter.drawLine(self.points[11][0] + 100, self.points[11][1] + 100, self.points[12][0] + 100,
                         self.points[12][1] + 100)

        # 食指
        painter.setPen(QPen(QColor(255, 0, 0), 4, Qt.SolidLine))
        for i in range(5, 8):
            painter.drawLine(self.points[i][0] + 100, self.points[i][1] + 100, self.points[i + 1][0] + 100,
                             self.points[i + 1][1] + 100)

        painter.setPen(QPen(QColor(0, 255, 0), 4, Qt.SolidLine))
        # 拇指
        for i in range(4):
            painter.drawLine(self.points[i][0]+100, self.points[i][1]+100, self.points[i+1][0]+100, self.points[i+1][1]+100)



        # # 设置画笔宽度
        # painter.setPen(QPen(QColor(0, 0, 0), 4, Qt.SolidLine))
        #
        # # 画圆点
        # for i in range(len(self.points)):
        #     painter.drawPoint(self.points[i][0]+150, self.points[i][1]+150)

        # # 分割线
        painter.setPen(QPen(QColor(0, 0, 0), 3, Qt.SolidLine))
        painter.drawLine(0, 200, self.screen_width, 200)

        # 设置字体大小
        painter.setFont(QFont('微软雅黑', 13))
        painter.drawText(25,235,'当前预测值 : '+ str(self.pred_value))



    def timerEvent(self, event) -> None:

        self.update()

    def enterEvent(self, event):
        self.hide_or_show('show', event)

    def leaveEvent(self, event):
        self.hide_or_show('hide', event)

    def hide_or_show(self, mode, event):
        # 获取窗口左上角x,y
        pos = self.frameGeometry().topLeft()
        if mode == 'show' and self.hidden:
            # 窗口左上角x + 窗口宽度 大于屏幕宽度，从右侧滑出
            if pos.x() + self.window_width >= self.screen_width:
                # 需要留10在里边，否则边界跳动
                self.startAnimation(self.screen_width - self.window_width, pos.y())
                event.accept()
                self.hidden = False
            # 窗口左上角x 小于0, 从左侧滑出
            elif pos.x() <= 0:
                self.startAnimation(0, pos.y())
                event.accept()
                self.hidden = False
            # 窗口左上角y 小于0, 从上方滑出
            elif pos.y() <= 0:
                self.startAnimation(pos.x(), 0)
                event.accept()
                self.hidden = False
        elif mode == 'hide' and (not self.hidden):
            if pos.x() + self.window_width >= self.screen_width:
                # 留10在外面
                self.startAnimation(self.screen_width - 10, pos.y(), mode, 'right')
                event.accept()
                self.hidden = True
            elif pos.x() <= 0:
                # 留10在外面
                self.startAnimation(10 - self.window_width, pos.y(), mode, 'left')
                event.accept()
                self.hidden = True
            elif pos.y() <= 0:
                # 留10在外面
                self.startAnimation(pos.x(), 10 - self.window_height, mode, 'up')
                event.accept()
                self.hidden = True

    def startAnimation(self, x, y, mode='show', direction=None):
        animation = QPropertyAnimation(self, b"geometry", self)
        # 滑出动画时长
        animation.setDuration(200)
        # 隐藏时，只留10在外边，防止跨屏
        # QRect限制其大小，防止跨屏
        num = QApplication.desktop().screenCount()
        if mode == 'hide':
            if direction == 'right':
                animation.setEndValue(QRect(x, y, 10, self.window_height))
            elif direction == 'left':
                # 多屏时采用不同的隐藏方法，防止跨屏
                if num < 2:
                    animation.setEndValue(QRect(x, y, self.window_width, self.window_height))
                else:
                    animation.setEndValue(QRect(0, y, 10, self.window_height))
            else:
                if num < 2:
                    animation.setEndValue(QRect(x, y, self.window_width, self.window_height))
                else:
                    animation.setEndValue(QRect(x, 0, self.window_width, 10))
        else:
            animation.setEndValue(QRect(x, y, self.window_width, self.window_height))
        animation.start()

    def mouseMoveEvent(self, event: QMouseEvent):
        # event.pos()减去最初相对窗口位置，获得移动距离(x,y)
        self._wmGap = event.pos() - self._startPos
        # 移动窗口，保持鼠标与窗口的相对位置不变
        # 检查是否移除了当前主屏幕
        # 左方界限
        final_pos = self.pos() + self._wmGap
        if self.frameGeometry().topLeft().x() + self._wmGap.x() <= 0:
            final_pos.setX(0)
        # 上方界限
        if self.frameGeometry().topLeft().y() + self._wmGap.y() <= 0:
            final_pos.setY(0)
        # 右方界限
        if self.frameGeometry().bottomRight().x() + self._wmGap.x() >= self.screen_width:
            final_pos.setX(self.screen_width - self.window_width)
        # 下方界限
        if self.frameGeometry().bottomRight().y() + self._wmGap.y() >= self.screen_height:
            final_pos.setY(self.screen_height - self.window_height)
        self.move(final_pos)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            # event.pos() 鼠标相对窗口的位置
            # event.globalPos() 鼠标在屏幕的绝对位置
            self._startPos = event.pos()
        if event.button() == Qt.RightButton:
            # 创建右键菜单
            menu = QMenu(self)
            menu.setStyleSheet(u"background-color: white;\n"
                               "selection-color: rgb(0, 255, 127);\n"
                               "selection-background-color: gray;\n"
                               "font: 8pt;")
            # 二级菜单
            size_menu = menu.addMenu('Bkcolor')
            light_gray = size_menu.addAction('Light-Gray')
            gray = size_menu.addAction('Gray')
            black = size_menu.addAction('Black')
            # 普通菜单
            quit_action = menu.addAction('Exit')
            about_action = menu.addAction('About')
            # 窗口定位到鼠标处
            action = menu.exec_(self.mapToGlobal(event.pos()))

            # 改变背景色
            if action == light_gray:
                self.setStyleSheet(u"background-color: rgb(100, 100, 100)")
            if action == gray:
                self.setStyleSheet(u"background-color: rgb(50, 50, 50)")
            if action == black:
                self.setStyleSheet(u"background-color: black")

            if action == quit_action:
                self.ui_alive = False
                QCoreApplication.quit()
            if action == about_action:
                # 新建MessageBox
                msg_box = QtWidgets.QMessageBox()
                # 支持HTML输入
                msg_box.about(self, "About", "<font size='3' color='white'>"
                                             "--------------------------"
                                             "<p>"
                                             "<i><b>Author: </b>Mingo.Meo</i>"
                                             "</p>"
                                             "<p>"
                                             "<i><b>Version: </b>1.0.0</i>"
                                             "</p>"
                                             "<p>"
                                             "<i><b>More: </b><a href='https://blog.csdn.net/weixin_44446598'>"
                                             "<span style='color:white'>Visit Me</span></a></i>"
                                             "</p>"
                                             "</font>")

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._startPos = None
            self._wmGap = None
        if event.button() == Qt.RightButton:
            self._startPos = None
            self._wmGap = None


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
