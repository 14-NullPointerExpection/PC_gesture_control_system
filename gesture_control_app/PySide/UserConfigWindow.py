'''
    @description: 用户自定义页面
    @Date: 2022-08-15
'''
import sys
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide.utils.MyMessageBox import MyMessageBox
from PySide.utils.PropertiesHandler import PropertyHandler
from PySide.utils.KeyboardMap import KeyboardMap

GESTURE_NUM = 4
SCROLL_BAR_WIDTH = 23


class CustomLineEdit(QtWidgets.QLineEdit):
    clicked = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def mousePressEvent(self, e):
        self.clicked.emit()


class UserConfigWindow(QLabel):
    def __init__(self, configs, parent=None):
        super().__init__(parent)
        self._configs = configs
        self._display = []
        self._select = []  # 下拉框
        self._label_select = []  # 标签
        self._input_area = []  # 文本框
        self._scroll_area = QScrollArea(self)
        self._display_area = QWidget(self)
        self._button_save = QPushButton(self)
        self._is_key_event_enable = False
        self._input_area_index = -1
        self._init_action = ['left_action', 'right_action', 'up_action', 'zero_action']
        self._key_to_index = {'press_key':0, 'open_url':1}
        self._init_action_key = ['left_action_key', 'right_action_key',
                                 'up_action_key', 'zero_action_key']
        self._init_action_url = ['left_action_url', 'right_action_url',
                                 'up_action_url', 'zero_action_url']
        self._image_path = ['PySide/resources/images/l.jpg', 'PySide/resources/images/r.jpg',
                            'PySide/resources/images/5.jpg', 'PySide/resources/images/0.jpg']
        self.initUI()

        # 引入qss文件
        with open('PySide/resources/qss/UserConfigWindow.qss', 'r') as f:
            self.setStyleSheet(f.read())

    def initUI(self):
        # 窗体样式
        self.show()
        self.setObjectName('UserConfigWindow')
        self.setGeometry(0, 0, 780, 500)

        # 展示区域
        display_interval = 180  # 每个展示框的间隔
        self._display_area.show()
        self._display_area.setObjectName('display_area')
        self._display_area.setGeometry(0, 0, self.width() - SCROLL_BAR_WIDTH, GESTURE_NUM * display_interval + 60)

        # 滚动条
        self._scroll_area.show()
        self._scroll_area.setWidget(self._display_area)
        self._scroll_area.setGeometry(0, 0, self.width(), self.height() - 100)
        # 隐藏横向滚动条
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
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
            # print(self._configs[self._init_action[i]])
            # print(self._key_to_index[self._configs[self._init_action[i]]])
            self._select[i].setCurrentIndex(self._key_to_index[self._configs[self._init_action[i]]])
            # 绑定下拉框的选择事件
            self._select[i].currentIndexChanged.connect(self.select_changed)
            # 文本框
            self._input_area.append(CustomLineEdit(self._display_area))
            self._input_area[i].setGeometry(QRect(420, 120 + i * display_interval, 200, 30))
            if self._key_to_index[self._configs[self._init_action[i]]] == 1:
                self._input_area[i].setText(self._configs[self._init_action_url[i]])
            else:
                self._input_area[i].setText(self._configs[self._init_action_key[i]])
                self.grabKeyboard()
                self._input_area[i].setReadOnly(True)
            self._input_area[i].show()
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
        self._button_save.clicked.connect(self.save_configs)

    def select_changed(self):
        # 获取当前选择的下拉框的索引
        index = self._select.index(self.sender())
        # 如果选择的是打开网页，则显示文本框
        if self._select[index].currentIndex() == 1:
            print('------------打开网页')
            self._input_area[index].setText(self._configs[self._init_action_url[index]])
            # 放开键盘
            self.releaseKeyboard()
            # 文本框可以编辑
            self._input_area[index].setReadOnly(False)
            # 解除绑定的键盘事件
            self._input_area[index].removeEventFilter(self)
            self._input_area[index].clicked.disconnect(self.input_area_clicked)

        else:
            print('------------快捷按键')
            self.grabKeyboard()
            self._input_area[index].setReadOnly(True)
            # 文本框绑定点击事件
            self._input_area[index].clicked.connect(self.input_area_clicked)
            self._input_area[index].setText(self._configs[self._init_action_key[index]])

    def input_area_clicked(self):
        self._is_key_event_enable = True
        self._input_area_index = self._input_area.index(self.sender())

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if not self._is_key_event_enable or self._input_area_index == -1:
            return
        # 获取当前文本框的索引
        key = event.key()
        if (key in KeyboardMap['qtkey_to_key'].keys()):
            self._input_area[self._input_area_index].setText(KeyboardMap['qtkey_to_key'][key])
        self._input_area_index = -1

    def save_configs(self):
        for i in range(GESTURE_NUM):
            if self._select[i].currentIndex() == 1:
                self._configs[self._init_action[i]] = 'open_url'
                self._configs[self._init_action_url[i]] = self._input_area[i].text()
            else:
                self._configs[self._init_action[i]] = 'press_key'
                self._configs[self._init_action_key[i]] = self._input_area[i].text()
                # self._init_action_key[i] = self._input_area[i].text()

        if PropertyHandler('settings.properties').save_properties(properties=self._configs) is None:
            self._message_box = MyMessageBox('配置文件已在其他文件中打开, 保存失败', 'error', self)
        else:
            self._message_box = MyMessageBox('保存成功', 'success', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = UserConfigWindow()
    w.show()
    w.move(300, 300)
    sys.exit(app.exec_())
