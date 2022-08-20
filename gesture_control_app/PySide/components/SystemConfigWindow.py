'''
    @description: 系统配置窗口
    @Date: 2022-08-16
'''
import sys

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from utils.MyMessageBox import MyMessageBox
from utils.PropertiesHandler import PropertyHandler


class SystemConfigWindow(QWidget):
    def __init__(self, configs, parent=None):
        super().__init__(parent)
        # 变量
        self._configs = configs
        self._labels = ['鼠标灵敏度', '页面滚动灵速率', '手势识别时间']
        self._label_keys = ['mouse_sensitivity', 'scroll_speed', 'gesture_recognition_speed']
        # 控件
        self._display_area = QLabel(self)
        self._sliders = []
        self._label_of_sliders = []
        self._spin_boxes = []
        self._button_save = QPushButton(self)
        self._message_box = None
        self.initUI()

        # 引入qss文件
        with open('PySide/resources/qss/SystemConfigWindow.qss', 'r') as f:
            self.setStyleSheet(f.read())

    def initUI(self):
        # 窗体样式
        self.show()
        self.setGeometry(0, 0, 750, 500)
        self.setObjectName('SystemConfigWindow')
        # 展示区域
        self._display_area.show()
        self._display_area.setObjectName('display_area')
        self._display_area.setGeometry(QRect(0, 0, 750, 500))

        start_x = 100
        start_y = 100

        for i in range(3):
            self._sliders.append(QSlider(Qt.Horizontal, self._display_area))
            self._label_of_sliders.append(QLabel(self._display_area))
            self._spin_boxes.append(QSpinBox(self._display_area))
            # 滑块
            self._sliders[i].setGeometry(QRect(start_x+170, start_y+10 + i * 80, 250, 30))
            self._sliders[i].setMinimum(1)
            self._sliders[i].setMaximum(100)
            self._sliders[i].setValue(self._configs[self._label_keys[i]])
            self._sliders[i].valueChanged.connect(self._spin_boxes[i].setValue)
            self._sliders[i].show()
            # 滑块标签
            self._label_of_sliders[i].setGeometry(QRect(start_x+10, start_y+10 + i * 80, 150, 30))
            self._label_of_sliders[i].setText(self._labels[i])
            self._label_of_sliders[i].show()
            # 滑块值
            self._spin_boxes[i].setGeometry(QRect(start_x+430, start_y+10 + i * 80, 50, 30))
            self._spin_boxes[i].setMinimum(1)
            self._spin_boxes[i].setMaximum(100)
            self._spin_boxes[i].setValue(self._configs[self._label_keys[i]])
            self._spin_boxes[i].valueChanged.connect(self._sliders[i].setValue)
            self._spin_boxes[i].show()
            

        # 按钮样式
        self._button_save.show()
        self._button_save.setGeometry(QRect(self.width()/2-50, self.height()-80, 100, 40))
        self._button_save.setText('保存')
        self._button_save.setCursor(QCursor(Qt.PointingHandCursor))
        self._button_save.clicked.connect(self.save_configs)
    
    def save_configs(self):
        for i in range(3):
            self._configs[self._label_keys[i]] = self._sliders[i].value()
        if PropertyHandler('settings.properties').save_properties(properties=self._configs) is None:
            self._message_box = MyMessageBox('配置文件已在其他文件中打开, 保存失败', 'error', self)
        else:
            self._message_box = MyMessageBox('保存成功', 'success', self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = SystemConfigWindow()
    w.show()
    w.move(300, 300)
    sys.exit(app.exec_())