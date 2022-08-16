import time

from GestureAlgorithm.Action.BaseAction import BaseAction
import pyautogui as pag


class LeftAction(BaseAction):
    def __init__(self):
        super().__init__()
        self._STOP_DURATION = 3

    def action(self):
        if time.time() - self._stop_time > self._STOP_DURATION:
            pag.press('left')
