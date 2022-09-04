"""
Author:匡俊骅

"""
import cgitb
import time
from time import sleep

import cv2
import cvzone
import pyautogui

from GestureAlgorithm import camera
from GestureAlgorithm.Action.BaseAction import BaseAction

cgitb.enable(format='text')

"""
虚拟键盘类，用以处理指定手势后弹出虚拟键盘的操作
"""


class VirtualKeyboard(BaseAction):
    # 按钮的类
    class Button:
        def __init__(self, pos, text, size=[85, 85]):
            self.pos = pos
            self.size = size
            self.text = text

    def __init__(self):
        super().__init__()
        # 所有按键
        self.keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                     ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", 'DEL'],
                     ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", 'OK']]
        # 最终输出的文本
        self.final_text = ""

        # 判断是否可以摧毁
        self.can_destroy = False

    # 绘制键盘
    def draw_all(self, image, button_list):
        # 绘制全部按钮
        for button in button_list:
            x, y = button.pos
            w, h = button.size
            cvzone.cornerRect(image, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                              20, rt=0)
            cv2.rectangle(image, button.pos, (x + w, y + h), (195, 150, 94), cv2.FILLED)
            # 绘制DEL键
            if button.text == 'DEL':
                cv2.putText(image, button.text, (x, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
                # 绘制OK键
            elif button.text == 'OK':
                cv2.putText(image, button.text, (x + 5, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
            else:
                # 绘制其他按键
                cv2.putText(image, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
        # 绘制下方输入框
        cv2.rectangle(image, (50, 350), (700, 450), (127, 172, 91), cv2.FILLED)
        cv2.putText(image, self.final_text, (60, 430),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
        return image

    def action(self, image, points):
        # 获取骨架图用以显示
        bone_image = camera.get_bone_image(image, points)

        # 获取全部按钮并缩放
        button_list = []
        for i in range(len(self.keys)):
            for j, key in enumerate(self.keys[i]):
                button_list.append(self.Button([100 * j + 50, 100 * i + 50], key))
        keyboard_image = self.draw_all(bone_image, button_list)

        if points:
            if self._can_action:
                # 对于获取的点根据视频尺寸缩放
                point = []
                for i in range(0, len(points)):
                    point.append((int(points[i][0] * image.shape[1]), int(points[i][1] * image.shape[0])))

                for button in button_list:
                    x, y = button.pos
                    w, h = button.size
                    # 手指虚点键盘
                    if x < point[8][0] < x + w and y < point[8][1] < y + h:
                        cv2.rectangle(keyboard_image, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 0, 175), cv2.FILLED)
                        cv2.putText(keyboard_image, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        distance = (pow((point[8][0] - point[12][0]), 2) + pow((point[8][1] - point[12][1]), 2)) ** 0.5
                        # 尝试进行点击操作
                        if distance < 30:
                            # 点击后的按钮颜色变化
                            cv2.rectangle(keyboard_image, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                            cv2.putText(keyboard_image, button.text, (x + 20, y + 65),
                                        cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                            self._can_action = False
                            self._stop_time = time.time()
                            # 对于特殊按钮的处理
                            if button.text == 'DEL':
                                self.final_text = self.final_text[:-1]
                            elif button.text == 'OK':
                                pyautogui.typewrite(self.final_text)
                                self.final_text = ''
                                self.can_destroy = True
                            else:
                                self.final_text += button.text
                            sleep(0.15)
            else:
                # 是否解除不应期
                if time.time() - self._stop_time > self._STOP_DURATION:
                    self._can_action = True
                    self._stop_time = 0

        cv2.waitKey(10)
        return self.can_destroy, keyboard_image
