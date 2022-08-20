import time

import pyautogui as pag

from GestureAlgorithm.Action.BaseAction import BaseAction
import webbrowser


# 字符串识别类，将字符串转化为配置文件对于操作
class StringAction(BaseAction):
    def __init__(self, command, properties):
        super().__init__()
        self.command = command
        # 将识别结果映射
        cmd_dict = {
            'l': 'left',
            'r': 'right',
            'u': 'up',
            '0': 'zero'
        }
        self.command = cmd_dict[self.command]
        self.properties = properties

    def action(self):
        if self._can_action:
            action_name = self.properties[self.command + '_action']
            if action_name == 'press_key':
                pag.press(self.properties[self.command + '_action_key'])
            elif action_name == 'open_url':
                webbrowser.open(self.properties[self.command + '_action_url'], new=0, autoraise=True)
            self._can_action = False
        else:
            if time.time() - self._stop_time > self._STOP_DURATION:
                self._can_action = True
                self._stop_time = 0
