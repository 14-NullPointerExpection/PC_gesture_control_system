"""
Author:匡俊骅
Description:鼠标的移动类
"""
import _thread
import time

import pyautogui as pag

from GestureAlgorithm.Action.BaseAction import BaseAction
from PySide.utils.PropertiesHandler import PropertyHandler

pag.FAILSAFE = False

'''
鼠标的移动类
'''


class MouseMoving(BaseAction):
    def __init__(self):
        super().__init__()
        self._last_x = 0
        self._last_y = 0
        self._last_click_time = 0
        self._CLICK_DURATION = 0.8
        self.properties = PropertyHandler('settings.properties').get_properties()
        self.mouse_sensitivity = self.properties['mouse_sensitivity'] / 45

    # 检测是否有点击的操作
    def try_click(self, points):
        if self._can_action:
            if abs(points[8][0] - points[12][0]) * 2560 < 80 and abs(points[8][1] - points[12][1]) * 1600 < 80:
                pag.click()
                self._last_click_time = time.time()
                self._can_action = False
        else:
            if time.time() - self._last_click_time > self._CLICK_DURATION:
                self._can_action = True
                self._last_click_time = 0
                self._stop_time = 0

    # points是手部坐标点的数组
    def action(self, points):
        if len(points) == 0:
            return
        # 当前食指尖的坐标
        x_r = points[8][0] * 2560
        y_r = points[8][1] * 1600
        # 如果是第一次进入这个函数，则将鼠标的位置设置为当前的位置
        if self._last_x == 0 and self._last_y == 0:
            self._last_x = x_r
            self._last_y = y_r

            return
        # 移动的相对坐标
        x_m = x_r - self._last_x
        y_m = y_r - self._last_y

        if self._can_action:
            if abs(x_m) < 15 and abs(y_m) < 15:
                self.try_click(points)
            else:
                _thread.start_new_thread(self.move, (x_m, y_m,points))
                # self.move(x_m, y_m, points)
        else:
            if time.time() - self._stop_time > self._STOP_DURATION:
                self._can_action = True
                self._stop_time = 0

        # 更新上次鼠标的位置
        self._last_x = x_r
        self._last_y = y_r

    # 移动鼠标
    def move(self, x_m, y_m, points):
        d = 0.1
        if abs(x_m) > 370 or abs(y_m) > 270:
            x_m = int(x_m * 4)
            y_m = int(y_m * 3.5)
            self._stop_time = time.time()
            self._can_action = False
            pag.moveRel(x_m, y_m, duration=0.25)
        elif abs(x_m) > 200 and abs(y_m) > 150:
            # 中速移动
            x_m = int(x_m * 3.4)
            y_m = int(y_m * 2.6)
            pag.moveRel(x_m, y_m, duration=0.1)
        elif abs(x_m) < 150 and abs(y_m) < 120:
            # 慢速移动
            x_m = int(x_m * 0.7)
            y_m = int(y_m * 0.5)
            pag.moveRel(x_m, y_m, duration=0.1)
        else:
            x_m = int(x_m * 2.5)
            y_m = int(y_m * 2.0)
            pag.moveRel(x_m, y_m, duration=0.1)
        # 鼠标灵敏度的修改
        # x_m = self.mouse_sensitivity*x_m
        # y_m = self.mouse_sensitivity*y_m



