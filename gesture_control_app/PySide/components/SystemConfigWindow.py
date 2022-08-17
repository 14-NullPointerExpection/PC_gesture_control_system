'''
    @description: 系统配置窗口
    @Date: 2022-08-16
'''
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys

class SystemConfigWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._slider_mouse_sensitivity = QSlider(self)
        self._slider_page_roll_sensitivity = QSlider(self)
        self._slider_gesture_time = QSlider(self)
        self._button_save = QPushButton(self)
        self.initUI()

        # 引入qss文件
        with open('resources/qss/SystemConfigWindow.qss', 'r') as f:
            self.setStyleSheet(f.read())

    def initUI(self):
        # 窗体样式
        self.show()
        self.setGeometry(0, 0, 800, 400)
        # 滑块样式
        self._slider_mouse_sensitivity.show()
        self._slider_mouse_sensitivity.setOrientation(Qt.Horizontal)
        self._slider_mouse_sensitivity.setGeometry(QRect(300, 150, 200, 30))

        self._slider_page_roll_sensitivity.show()
        self._slider_page_roll_sensitivity.setOrientation(Qt.Horizontal)
        self._slider_page_roll_sensitivity.setGeometry(QRect(300, 230, 200, 30))

        self._slider_gesture_time.show()
        self._slider_gesture_time.setOrientation(Qt.Horizontal)
        self._slider_gesture_time.setGeometry(QRect(300, 310, 200, 30))

        # 按钮样式
        self._button_save.show()
        self._button_save.setGeometry(QRect(300, 360, 100, 40))
        self._button_save.setText('保存')

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2))
        painter.drawText(QRect(200, 110, 60, 30), Qt.AlignCenter, '鼠标移动')
        painter.drawText(QRect(230, 145, 60, 30), Qt.AlignCenter, '灵敏度')
        painter.drawText(QRect(200, 190, 60, 30), Qt.AlignCenter, '页面滚动')
        painter.drawText(QRect(230, 225, 60, 30), Qt.AlignCenter, '滚动速率')
        painter.drawText(QRect(200, 270, 60, 30), Qt.AlignCenter, '手势')
        painter.drawText(QRect(200, 305, 90, 30), Qt.AlignCenter, '手势识别时间')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SystemConfigWindow()
    w.show()
    w.move(300, 300)
    sys.exit(app.exec_())