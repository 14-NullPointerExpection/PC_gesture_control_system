'''
    @description: 用户自定义页面
    @Date: 2022-08-15
'''
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
import sys

GESTURE_NUM = 3
SCROLL_BAR_WIDTH = 23

class UserConfigWindow(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self._display = [] # 展示窗口
        self._select = [] # 下拉框
        self._label_select = [] # 标签
        self._scroll_area = QScrollArea(self)
        self._display_area = QWidget(self)
        self._button_save = QPushButton(self)
        self.initUI()

        # 引入qss文件
        with open('PySide/resources/qss/UserConfigWindow.qss', 'r') as f:
            self.setStyleSheet(f.read())


    def initUI(self):
        # 窗体样式
        self.show()
        self.setObjectName('UserConfigWindow')
        self.setGeometry(0, 0, 750, 500)

        # 展示区域
        display_interval = 180 # 每个展示框的间隔
        self._display_area.show()
        self._display_area.setObjectName('display_area')
        self._display_area.setGeometry(0, 0, self.width() - 23, GESTURE_NUM * display_interval + 60)

        # 滚动条
        self._scroll_area.show()
        self._scroll_area.setWidget(self._display_area)
        self._scroll_area.setGeometry(0, 0, self.width(), self.height()-100)

        
        for i in range(GESTURE_NUM):
            # 显示框样式
            self._display.append(QLabel(self._display_area))
            self._display[i].show()
            self._display[i].setObjectName('display_board')
            self._display[i].setGeometry(QRect(80, 30+i*display_interval, 150, 150))
            # 下拉框样式
            self._select.append(QComboBox(self._display_area))
            self._select[i].show()
            self._select[i].setGeometry(QRect(420, 80+i*display_interval, 200, 30))
            self._select[i].addItem('选项1')
            self._select[i].addItem('选项2')
            # 标签样式
            self._label_select.append(QLabel(self._display_area))
            self._label_select[i].show()
            self._label_select[i].setObjectName('label_select')
            self._label_select[i].setGeometry(QRect(320, 80+i*display_interval, 80, 30))
            self._label_select[i].setText('功能选择')
    
        # 保存按钮样式
        self._button_save.show()
        self._button_save.setGeometry(QRect(self.width()/2-50, self.height()-80, 100, 40))
        self._button_save.setCursor(Qt.PointingHandCursor)
        self._button_save.setText('保存')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = UserConfigWindow()
    w.show()
    w.move(300, 300)
    sys.exit(app.exec_())