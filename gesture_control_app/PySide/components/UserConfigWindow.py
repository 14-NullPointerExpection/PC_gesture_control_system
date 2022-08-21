'''
    @description: 用户自定义页面
    @Date: 2022-08-15
'''
import sys
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

GESTURE_NUM = 4
SCROLL_BAR_WIDTH = 23


class CustomLineEdit(QtWidgets.QLineEdit):
    clicked = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, e):
        self.clicked.emit()


class UserConfigWindow(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._display = []
        self._select = []  # 下拉框
        self._label_select = []  # 标签
        self._input_area = []  # 文本框
        self._scroll_area = QScrollArea(self)
        self._display_area = QWidget(self)
        self._button_save = QPushButton(self)
        self._is_key_event_enable = False
        self._input_area_index = -1
        self._image_path = ['PySide/resources/images/0.jpg', 'PySide/resources/images/5.jpg',
                            'PySide/resources/images/l.jpg', 'PySide/resources/images/r.jpg']
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
        display_interval = 180  # 每个展示框的间隔
        self._display_area.show()
        self._display_area.setObjectName('display_area')
        self._display_area.setGeometry(0, 0, self.width() - 23, GESTURE_NUM * display_interval + 60)

        # 滚动条
        self._scroll_area.show()
        self._scroll_area.setWidget(self._display_area)
        self._scroll_area.setGeometry(0, 0, self.width(), self.height() - 100)

        for i in range(GESTURE_NUM):
            # 显示框样式

            self._display.append(QLabel(self._display_area))
            self._display[i].show()
            self._display[i].setObjectName('display_board')
            self._display[i].setGeometry(QRect(80, 30 + i * display_interval, 150, 150))
            pixmap = QPixmap(QPixmap(self._image_path[i]))
            self._display[i].setPixmap(pixmap)
            self._display[i].setScaledContents(True)
            # 下拉框样式
            self._select.append(QComboBox(self._display_area))
            self._select[i].show()
            self._select[i].setGeometry(QRect(420, 80 + i * display_interval, 200, 30))
            self._select[i].addItem('快捷按键')
            self._select[i].addItem('打开网页')
            # 绑定下拉框的选择事件
            self._select[i].currentIndexChanged.connect(self.select_changed)
            # 文本框
            self._input_area.append(CustomLineEdit(self._display_area))
            self._input_area[i].setGeometry(QRect(420, 120 + i * display_interval, 200, 30))
            self._input_area[i].show()
            self._input_area[i].setReadOnly(True)
            # 文本框绑定点击事件
            self._input_area[i].clicked.connect(self.input_area_clicked)
            # 标签样式
            self._label_select.append(QLabel(self._display_area))
            self._label_select[i].show()
            self._label_select[i].setObjectName('label_select')
            self._label_select[i].setGeometry(QRect(320, 80 + i * display_interval, 80, 30))
            self._label_select[i].setText('功能选择')

        # 保存按钮样式
        self._button_save.show()
        self._button_save.setGeometry(QRect(self.width() / 2 - 50, self.height() - 80, 100, 40))
        self._button_save.setCursor(Qt.PointingHandCursor)
        self._button_save.setText('保存')

    def select_changed(self):
        # 获取当前选择的下拉框的索引
        index = self._select.index(self.sender())
        self._input_area[index].setText('')
        # 如果选择的是打开网页，则显示文本框
        if self._select[index].currentIndex() == 1:

            print('------------打开网页')
            # 放开键盘
            self.releaseKeyboard()
            # 文本框可以编辑
            self._input_area[index].setReadOnly(False)
            # 解除绑定的键盘事件
            self._input_area[index].removeEventFilter(self)

        else:
            print('------------快捷按键')
            self.grabKeyboard()
            self._input_area[index].setReadOnly(True)
            # 文本框绑定点击事件
            self._input_area[index].clicked.connect(self.input_area_clicked)

    def input_area_clicked(self):
        self._is_key_event_enable = True
        self._input_area_index = self._input_area.index(self.sender())

    def keyPressEvent(self, event):
        if not self._is_key_event_enable or self._input_area_index == -1:
            return
        # 获取当前文本框的索引
        if event.key() == Qt.Key_Escape:
            self._input_area[self._input_area_index].setText('ESC')
        if event.key() == Qt.Key_Up:
            self._input_area[self._input_area_index].setText('UP')
        if event.key() == Qt.Key_Down:
            self._input_area[self._input_area_index].setText('DOWN')
        if event.key() == Qt.Key_Left:
            self._input_area[self._input_area_index].setText('LEFT')
        if event.key() == Qt.Key_Right:
            self._input_area[self._input_area_index].setText('RIGHT')
        if event.key == Qt.Key_Backspace:
            self._input_area[self._input_area_index].setText('BACKSPACE')
        # a到z
        if (event.key() >= Qt.Key_A and event.key() <= Qt.Key_Z):
            self._input_area[self._input_area_index].setText(chr(event.key()))
        # a 到z的大写
        if (event.key() >= Qt.Key_A and event.key() <= Qt.Key_Z and event.modifiers() == Qt.ShiftModifier):
            self._input_area[self._input_area_index].setText(chr(event.key()).upper())
        # 0到9
        if (event.key() >= Qt.Key_0 and event.key() <= Qt.Key_9):
            self._input_area[self._input_area_index].setText(chr(event.key()))

        self._input_area_index = -1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = UserConfigWindow()
    w.show()
    w.move(300, 300)
    sys.exit(app.exec_())
