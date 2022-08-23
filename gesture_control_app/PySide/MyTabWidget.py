'''
    @description: MyTabWidget
    @Date: 2020-08-23
'''

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class MyTabWidget(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._last_index = 0
        self._current_index = 0
        self._status = 'none'
        self._ischange = False
        self._move_speed = 1.0
        QTimer.singleShot(100, lambda : self.change_status('none', True))
        self._effect_animation = []
        self.ANIMATION_DURATION = 700
        # 切换事件
        self.tabBar().currentChanged.connect(self.on_current_changed)
        self.startTimer(10)
        # 过滤器
        self.tabBar().installEventFilter(self)
    
    def on_current_changed(self, index):
        if not self._ischange:
            return
        self._effect_animation = []
        if self._status == 'none':
            self.change_status('disappear', False)
            self.setCurrentIndex(self._last_index)
            self._current_index = index
            # 渐变消失动画
            w = self.currentWidget()
            w1 = w.findChild(QWidget, 'display_area')
            self.create_animation(w)
            self.create_animation(w1)
            self.change_status('change', True)
            QTimer.singleShot(self.ANIMATION_DURATION, lambda : self.setCurrentIndex(self._current_index))
        elif self._status == 'change':
            self.change_status('appear', False)
            self._last_index = index
            w = self.currentWidget()
            w1 = w.findChild(QWidget, 'display_area')
            self.create_animation(w)
            self.create_animation(w1)
            QTimer.singleShot(self.ANIMATION_DURATION, lambda : self.change_status('none', True))
            w.move(w.x(), -w.height())
            self._move_speed = w.height() / (self.ANIMATION_DURATION/10)



    def create_animation(self, widget):
        if (self._status == 'disappear'):
            start_opacity = 0.99
            end_opacity = 0.1
        else:
            start_opacity = 0.1
            end_opacity = 0.99
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        animation = QPropertyAnimation(effect, b'opacity')
        animation.setDuration(self.ANIMATION_DURATION)
        animation.setStartValue(start_opacity)
        animation.setEndValue(end_opacity)
        animation.start(QAbstractAnimation.DeleteWhenStopped)
        self._effect_animation.append(animation)


    def timerEvent(self, event: QTimerEvent) -> None:
        if self._status == 'none' or self._status == 'change':
            return
            
        if self._status == 'disappear':
            pass
        elif self._status == 'appear':
            w = self.currentWidget()
            if w.y() >= 0:
                w.move(w.x(), 0)
            else:
                w.move(w.x(), w.y() + self._move_speed)

    def change_status(self, status, ischange):
        self._status = status
        self._ischange = ischange
    
    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if watched == self.tabBar():
            if event.type() == QEvent.MouseButtonPress and self._status != 'none':
                return True
        return False

