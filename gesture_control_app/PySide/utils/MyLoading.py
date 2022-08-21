'''
    @description: MyLoading加载
    @Date: 2022-08-20
'''

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

WIDTH = 400
HEIGHT = 400
LABEL_WIDTH = 150
LABEL_HEIGHT = 150

class MyLoading(QLabel):
    def __init__(self, text='加载中', parent=None):
        super().__init__(parent)
        self._text = text
        self._animation = QMovie('PySide/resources/images/loading.gif')
        self._label_animation = QLabel(self)
        self.init_ui()

    def init_ui(self):
        # 设置窗口无边框且置于顶层
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow | Qt.WindowStaysOnTopHint)
        # 窗口位置
        if (self.parent() is not None):
            point_x = 0
            point_y = 0
            self.setFixedSize(self.parent().width(), self.parent().height())
        else:
            self.setFixedSize(WIDTH, HEIGHT)
            point_x = QApplication.desktop().width()//2 - WIDTH//2
            point_y = QApplication.desktop().height()//2 - HEIGHT//3*2
        self.move(point_x, point_y)
        self.show()
        # 动画窗口
        self._label_animation.setMovie(self._animation)
        self._label_animation.setGeometry(self.width()//2 - LABEL_WIDTH//2, self.height()//2 - LABEL_HEIGHT//2, LABEL_WIDTH, LABEL_HEIGHT)
        self._label_animation.setScaledContents(True)
        self._label_animation.show()
        self._animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        # 绘制背景色
        painter.setBrush(QBrush(QColor(213, 248, 252, 150)))
        painter.drawRect(self.rect())
        # 加载中文字
        painter.setPen(QPen(QColor(10, 10, 10)))
        painter.setFont(QFont('Microsoft YaHei', 15))
        painter.drawText(QRect(self.width()//2 - 100, self.height()//2 + 70, 200, 40), Qt.AlignCenter, self._text)


    
    def stop(self):
        self._animation.stop()
        self.deleteLater()