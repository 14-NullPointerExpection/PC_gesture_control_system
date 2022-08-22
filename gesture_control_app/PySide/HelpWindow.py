'''
    @description: 帮助窗口
    @Date: 2022-08-22
'''

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

SCROLL_BAR_WIDTH = 23

class HelpWindow(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._scroll_area = QScrollArea(self)
        self._display_area = QWidget(self)
        self._title1 = QLabel(self._display_area)
        self._title2 = QLabel(self._display_area)
        self._title3 = QLabel(self._display_area)
        self._content1 = QLabel(self._display_area)
        self._content2 = QLabel(self._display_area)
        self._content3 = QLabel(self._display_area)
        self.init_ui()
        
        # 引入样式
        with open('PySide/resources/qss/HelpWindow.qss', 'r') as f:
            self.setStyleSheet(f.read())

    def init_ui(self):
        # 窗体样式
        self.show()
        self.setGeometry(0, 0, 780, 500)
        self.setObjectName('HelpWindow')
        
        # 展示区域
        self._display_area.show()
        self._display_area.setObjectName('display_area')
        self._display_area.setGeometry(0, 0, self.width() - SCROLL_BAR_WIDTH, self.height()+200)

        # 滚动条
        self._scroll_area.show()
        self._scroll_area.setWidget(self._display_area)
        self._scroll_area.setGeometry(0, 0, self.width(), self.height() - 5)
        # 隐藏横向滚动条
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        start_x = 20
        start_y = 20

        # 标题
        self._title1.setObjectName('title')
        self._title1.setGeometry(start_x, start_y, 200, 35)
        self._title1.setText('鼠标控制模式')

        self._title2.setObjectName('title')
        self._title2.setGeometry(start_x, start_y + 320, 200, 35)
        self._title2.setText('快捷手势模式')

        self._title3.setObjectName('title')
        self._title3.setGeometry(start_x, start_y + 480, 200, 35)
        self._title3.setText('其他说明')

        # 内容
        self._content1.setObjectName('content')
        self._content1.setGeometry(start_x, start_y + 20, 700, 300)
        content1 = '''
        ● 点击"启动鼠标控制"即可进入鼠标控制模式
        ● 五个手指全张开摆成数字五, 即可切换鼠标移动状态与上下滑动状态
        ● 鼠标移动状态下, 伸出食指朝某个方向滑动, 可以控制鼠标往该方向移动
                手指滑动的越快, 鼠标移动的幅度越大
                可以在系统设置中调节鼠标灵敏度
                用中指轻碰食指, 可以进行鼠标点击
                食指中指摆出"V"形, 可以打开悬浮键盘
        ● 上下滑动状态下, 用食指向上或向下滑动, 即可实现页面的上下滚动
                可以在系统设置中调节页面滚动速度
        ● 点击"停止"按钮或者按下F1键, 可以退出鼠标控制模式
        '''
        self._content1.setText(content1)

        self._content2.setObjectName('content')
        self._content2.setGeometry(start_x, start_y + 260, 700, 300)
        content2 = '''
        ● 点击"启动快捷键控制"即可进入快捷手势模式
        ● 快捷手势可以在用户自定义界面中查看并设置
        ● 快捷手势可以设置成快捷键和打开网址两种功能
        ● 点击"停止"按钮或者按下F1键, 可以退出快捷手势模式
        '''
        self._content2.setText(content2)

        self._content3.setObjectName('content')
        self._content3.setGeometry(start_x, start_y + 390, 700, 300)
        content3 = '''
        ● 如果手势识别速度过慢或过快, 可以在系统设置中调节手势识别时间
        ● 所有设置均须保存后才能生效
        '''
        self._content3.setText(content3)
