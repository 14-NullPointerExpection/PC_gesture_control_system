import time

import pyautogui as pag

from GestureAlgorithm.Action.BaseAction import BaseAction
import webbrowser


# 字符串识别类，将字符串转化为配置文件对应操作
class StringAction(BaseAction):
    def __init__(self, properties):
        super().__init__()
        # 将识别结果映射
        self.cmd_dict = {
            'l': 'left',
            'r': 'right',
            'u': 'up',
            '0': 'zero'
        }
        self.properties = properties
        self._STOP_DURATION = 2
        self.command = None

    def set_command(self, command):
        self.command = command
        self.command = self.cmd_dict[self.command]

    def action(self):
        if self._can_action:
            action_name = self.properties[self.command + '_action']
            if action_name == 'press_key':
                pag.press(self.properties[self.command + '_action_key'])
            elif action_name == 'open_url':
                webbrowser.open(self.properties[self.command + '_action_url'], new=0, autoraise=True)
            self._can_action = False
            self._stop_time = time.time()
        else:
            if time.time() - self._stop_time > self._STOP_DURATION:
                self._can_action = True
