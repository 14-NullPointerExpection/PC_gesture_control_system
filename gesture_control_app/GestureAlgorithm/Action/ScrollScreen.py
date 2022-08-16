"""
Author:匡俊骅
Description:对屏幕进行滚动操作
"""
import pyautogui as pag
from action import Action


class ScrollScreen(Action):

    def __init__(self):
        super().__init__()
        # 鼠标上次的位置
        self._last_y = 0

    def action(self, _, y_r):
        if self._last_y == 0:
            self._last_y = y_r
        else:
            # 移动的相对坐标
            y_m = y_r - self._last_y
            if abs(y_m) > 500:
                print("滑动")
                pag.scroll(int(y_m * 1.5))
