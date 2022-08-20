import time

import pyautogui as pag

from GestureAlgorithm.Action.BaseAction import BaseAction


class LeftAction(BaseAction):
    def __init__(self):
        super().__init__()
        self._STOP_DURATION = 3

    def action(self):
        if time.time() - self._stop_time > self._STOP_DURATION:
            pag.press('left')
