import time

import pyautogui as pag

from GestureAlgorithm.Action.BaseAction import BaseAction


class RightAction(BaseAction):
    def __init__(self):
        super().__init__()

    def action(self):
        if time.time() - self._stop_time > self._STOP_DURATION:
            pag.press('right')
