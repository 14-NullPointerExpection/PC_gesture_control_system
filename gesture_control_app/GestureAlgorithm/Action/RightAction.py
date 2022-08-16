import time

from GestureAlgorithm.Action.BaseAction import BaseAction
import pyautogui as pag


class RightAction(BaseAction):
    def __init__(self):
        super().__init__()

    def action(self):
        if time.time() - self._stop_time > self._STOP_DURATION:
            pag.press('right')
