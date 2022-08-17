'''
    @description: MyMessageBox类
    @Date: 2020-08-17
'''

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

WIDTH = 300
HEIGHT = 50

class MyMessageBox(QLabel):
    def __init__(self, message, type='info', parent=None):
        super().__init__()
        self.setText(message)
        self._type = type
        self._parent = parent
        colors = {
            'info': QColor(100, 100, 100),
            'error': QColor(255, 0, 0),
            'success': QColor(240, 249, 235)
        }
        font_colors = {
            'info': 'rgb(255, 255, 255)',
            'error': 'rgb(255, 255, 255)',
            'success': 'rgb(103, 194, 58)'
        }
        if (type not in colors):
            self._type = 'info'
        self._color = colors[self._type]
        self._font_color = font_colors[self._type]
        self._opacity = 0.0
        self._timer = 0

        self.init_ui()

        self.startTimer(10)

    def init_ui(self):
        # 设置背景色
        palette = QPalette()
        palette.setColor(QPalette.Window, self._color)
        self.setPalette(palette)
        self.setWindowOpacity(self._opacity)
        # 设置窗口无边框且置于顶层
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow | Qt.WindowStaysOnTopHint)
        # 窗口大小
        self.setFixedSize(WIDTH, HEIGHT)
        # 窗口位置
        if (self._parent is not None):
            point_x = self._parent.width() // 2
            point_y = 0
            p = self._parent
            while (p is not None):
                point_x += p.x()
                point_y += p.y()
                p = p.parent()
        else:
            point_x = QApplication.desktop().width()//2 - WIDTH//2
            point_y = QApplication.desktop().height()//2 - HEIGHT//3*2
        self.move(point_x - WIDTH/2, point_y)
        # 字体
        font = QFont('Microsoft YaHei', 12, QFont.Bold)
        self.setFont(font)
        # 字体颜色
        self.setStyleSheet('color: %s' % self._font_color)
        # 居中
        self.setAlignment(Qt.AlignCenter)

        self.show()
        

    def timerEvent(self, event: QTimerEvent) -> None:
        self._timer += 1
        if (self._timer < 50):
            self._opacity = min(self._opacity + 0.02, 1.0)
            self.setWindowOpacity(self._opacity)
            self.move(self.x(), self.y()+1)
        elif (self._timer < 150):
            pass
        elif (self._timer < 200):
            self._opacity = max(self._opacity - 0.02, 0.0)
            self.setWindowOpacity(self._opacity)
            self.move(self.x(), self.y()-1)
        else:
            self.deleteLater()
            
            
