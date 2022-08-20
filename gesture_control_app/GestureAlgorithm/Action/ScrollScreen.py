"""
Author:匡俊骅
Description:对屏幕进行滚动操作
"""
import time

import pyautogui as pag

from GestureAlgorithm.Action.BaseAction import BaseAction
from PySide.utils.PropertiesHandler import PropertyHandler


class ScrollScreen(BaseAction):
    def __init__(self):
        super().__init__()
        # 手指上次的位置
        # self._last_stop_time = None
        self._last_y = 0
        self.properties = PropertyHandler('settings.properties').get_properties()
        self.scroll_speed = self.properties['scroll_speed']
        self._STOP_DURATION = 2

    def action(self, points):
        if len(points) == 0:
            return

        y_r = points[8][1] * 1600
        if self._can_action:
            if self._last_y == 0:
                self._last_y = y_r
            else:
                # 移动的相对坐标
                y_m = y_r - self._last_y
                if abs(y_m) > 500:
                    pag.scroll(int(y_m * 1.5))
                    self._stop_time = time.time()
                    self._can_action = False
                self._last_y = y_r
        else:
            if time.time() - self._stop_time > self._STOP_DURATION:
                self._can_action = True
                self._stop_time = 0
