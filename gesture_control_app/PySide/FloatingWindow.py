"""
author: XP
desc: 悬浮窗的基类, 用于实现悬浮窗的基本功能
"""
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class FloatingWindow(QWidget):
    def __init__(self, parent=None):
        super(FloatingWindow, self).__init__(parent)
        # # 设置窗口无边框； 设置窗口置顶；
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        # 设置透明度(0~1)
        self.setWindowOpacity(0.5)
        # 设置鼠标为手状
        self.setCursor(Qt.PointingHandCursor)
        # self.timer = 0
        self._startPos = None
        self._wmGap = None
        # 悬浮窗是否隐藏
        self._hidden = False
        dsk = QApplication.primaryScreen()
        self._screen_width = dsk.geometry().width()
        self._screen_height = dsk.geometry().height()
        self.WINDOW_WIDTH = 300
        self.WINDOW_HEIGHT = 300
        # 设置悬浮窗刷新间隔
        self.startTimer(100)

    # 定时刷新悬浮窗
    def timerEvent(self, event) -> None:
        self.update()

    # 鼠标进入悬浮窗
    def enterEvent(self, event):
        self.hideOrShow('show', event)

    # 鼠标离开悬浮窗
    def leaveEvent(self, event):
        self.hideOrShow('hide', event)

    # 判断悬浮窗是否隐藏
    def hideOrShow(self, mode, event):
        # 获取窗口左上角x,y
        pos = self.frameGeometry().topLeft()
        if mode == 'show' and self._hidden:
            # 窗口左上角x + 窗口宽度 大于屏幕宽度，从右侧滑出
            if pos.x() + self.WINDOW_WIDTH >= self._screen_width:
                # 需要留10在里边，否则边界跳动
                self.startAnimation(self._screen_width - self.WINDOW_WIDTH, pos.y())
                event.accept()
                self._hidden = False
            # 窗口左上角x 小于0, 从左侧滑出
            elif pos.x() <= 0:
                self.startAnimation(0, pos.y())
                event.accept()
                self._hidden = False
            # 窗口左上角y 小于0, 从上方滑出
            elif pos.y() <= 0:
                self.startAnimation(pos.x(), 0)
                event.accept()
                self._hidden = False
        elif mode == 'hide' and (not self._hidden):
            if pos.x() + self.WINDOW_WIDTH >= self._screen_width:
                # 留10在外面
                self.startAnimation(self._screen_width - 10, pos.y(), mode, 'right')
                event.accept()
                self._hidden = True
            elif pos.x() <= 0:
                # 留10在外面
                self.startAnimation(10 - self.WINDOW_WIDTH, pos.y(), mode, 'left')
                event.accept()
                self._hidden = True
            elif pos.y() <= 0:
                # 留10在外面
                self.startAnimation(pos.x(), 10 - self.WINDOW_HEIGHT, mode, 'up')
                event.accept()
                self._hidden = True

    # 滑动效果
    def startAnimation(self, x, y, mode='show', direction=None):
        animation = QPropertyAnimation(self, b'geometry', self)
        # 滑出动画时长
        animation.setDuration(200)
        # 隐藏时，只留10在外边，防止跨屏
        # QRect限制其大小，防止跨屏
        num = QApplication.desktop().screenCount()
        if mode == 'hide':
            if direction == 'right':
                animation.setEndValue(QRect(x, y, 10, self.WINDOW_HEIGHT))
            elif direction == 'left':
                # 多屏时采用不同的隐藏方法，防止跨屏
                if num < 2:
                    animation.setEndValue(QRect(x, y, self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
                else:
                    animation.setEndValue(QRect(0, y, 10, self.WINDOW_HEIGHT))
            else:
                if num < 2:
                    animation.setEndValue(QRect(x, y, self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
                else:
                    animation.setEndValue(QRect(x, 0, self.WINDOW_WIDTH, 10))
        else:
            animation.setEndValue(QRect(x, y, self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
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
        if self.frameGeometry().bottomRight().x() + self._wmGap.x() >= self._screen_width:
            final_pos.setX(self._screen_width - self.WINDOW_WIDTH)
        # 下方界限
        if self.frameGeometry().bottomRight().y() + self._wmGap.y() >= self._screen_height:
            final_pos.setY(self._screen_height - self.WINDOW_HEIGHT)
        self.move(final_pos)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            # event.pos() 鼠标相对窗口的位置
            # event.globalPos() 鼠标在屏幕的绝对位置
            self._startPos = event.pos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self._startPos = None
            self._wmGap = None
        if event.button() == Qt.RightButton:
            self._startPos = None
            self._wmGap = None
