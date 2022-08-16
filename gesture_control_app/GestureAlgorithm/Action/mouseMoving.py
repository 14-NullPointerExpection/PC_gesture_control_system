"""
Author:匡俊骅
Description:鼠标的移动类
"""

import time
import pyautogui as pag
import logging
import Action.BaseAction
pag.FAILSAFE = False


'''
鼠标的移动类
'''


class MouseMoving(Action.BaseAction.BaseAction):
    def __init__(self):
        super().__init__()
        # # 鼠标应该停止移动的时间点
        # self._stop_time = 0
        # # 鼠标停止移动的持续时间
        # self._STOP_DURATION = 0.5
        # # 鼠标是否可以移动
        # self._can_move = True
        # 鼠标上次的位置

        self._last_x = 0
        self._last_y = 0

    # x_r是当前鼠标的x坐标，y_r是当前鼠标的y坐标
    def action(self, points):
        x_r = points[8][0]*2560
        y_r = points[8][1]*1600

        # 如果是第一次进入这个函数，则将鼠标的位置设置为当前的位置
        if self._last_x == 0 and self._last_y == 0:
            self._last_x = x_r
            self._last_y = y_r
            return
        # 移动的相对坐标
        x_m = x_r - self._last_x
        y_m = y_r - self._last_y
        d = 0.1
        if self._can_action:
            if abs(x_m) > 370 or abs(y_m) > 270:
                x_m = int(x_m * 4)
                y_m = int(y_m * 3.5)
                pag.moveRel(x_m, y_m, duration=0.25)
                # 如果鼠标移动的距离大于一定的距离，那么鼠标就不能移动
                self._stop_time = time.time()
                self._can_action = False
            elif abs(x_m) > 200 and abs(y_m) > 150:
                # print("中速移动")
                x_m = int(x_m * 3.4)
                y_m = int(y_m * 2.6)
                pag.moveRel(x_m, y_m, duration=d)
            elif abs(x_m) < 150 and abs(y_m) < 120:
                # print("慢速移动")
                x_m = int(x_m * 0.7)
                y_m = int(y_m * 0.5)
                pag.moveRel(x_m, y_m, duration=d)
            else:
                x_m = int(x_m * 2.5)
                y_m = int(y_m * 2.0)
                pag.moveRel(x_m, y_m, duration=d)
        else:
            if time.time() - self._stop_time > self._STOP_DURATION:
                self._can_action = True
                self._last_x = 0
                self._last_y = 0
                self._stop_time = 0

        # 更新上次鼠标的位置
        self._last_x = x_r
        self._last_y = y_r
    
