"""
Author:匡俊骅

"""
import time
from time import sleep

import cv2
import cvzone
import pyautogui

from GestureAlgorithm.Action.BaseAction import BaseAction
from GestureAlgorithm.camera import Camera, MOUSE_CONTROL_MODE, MOUSE_MOVING


def singleton(cls):
    _instance = {}

    def inner():
        if cls not in _instance:
            _instance[cls] = cls()
        return _instance[cls]

    return inner


@singleton
class VirtualKeyboard(BaseAction):
    class Button:
        def __init__(self, pos, text, size=[85, 85]):
            self.pos = pos
            self.size = size
            self.text = text

    def __init__(self):
        super().__init__()
        self.keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                     ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", 'DEL'],
                     ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", 'OK']]
        self.final_text = ""
        self.camera = None
        self.can_destroy = False

    def set_camera(self, camera):
        self.camera = camera

    def draw_all(self, image, button_list):
        cv2.rectangle(image, (50, 350), (700, 450), (127, 172, 91), cv2.FILLED)
        cv2.putText(image, self.final_text, (60, 430),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)
        for button in button_list:
            x, y = button.pos
            w, h = button.size
            cvzone.cornerRect(image, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                              20, rt=0)
            cv2.rectangle(image, button.pos, (x + w, y + h), (195, 150, 94), cv2.FILLED)
            if button.text == 'DEL':
                cv2.putText(image, button.text, (x, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
            elif button.text == 'OK':
                cv2.putText(image, button.text, (x + 5, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
            else:
                cv2.putText(image, button.text, (x + 20, y + 65),
                            cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 4)
        return image

    def action(self, image, points):


        bone_image = self.camera.get_bone_image(image)

        button_list = []
        for i in range(len(self.keys)):
            for j, key in enumerate(self.keys[i]):
                button_list.append(self.Button([100 * j + 50, 100 * i + 50], key))
        keyboard_image = self.draw_all(bone_image, button_list)

        if points:
            if self._can_action:
                # points = list(map(lambda p: (int(p[0] * image[0]), int(p[1] * image[1])), points))
                point = []
                for i in range(0, len(points)):
                    point.append((int(points[i][0] * image.shape[1]), int(points[i][1] * image.shape[0])))

                for button in button_list:
                    x, y = button.pos
                    w, h = button.size
                    # 手指虚点键盘

                    if x < point[8][0] < x + w and y < point[8][1] < y + h:
                        print("虚点",button.text)
                        cv2.rectangle(keyboard_image, (x - 5, y - 5), (x + w + 5, y + h + 5), (0, 0, 175), cv2.FILLED)
                        cv2.putText(keyboard_image, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        # l, _, _ = detector.findDistance(8, 12, img, draw=False)
                        l = (pow((point[8][0] - point[12][0]), 2) + pow((point[8][1] - point[12][1]), 2)) ** 0.5

                        # 尝试进行点击操作
                        if l < 30:

                            cv2.rectangle(keyboard_image, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                            cv2.putText(keyboard_image, button.text, (x + 20, y + 65),
                                        cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                            self._can_action = False
                            self._stop_time = time.time()


                            if button.text == 'DEL':
                                self.final_text = self.final_text[:-1]
                            elif button.text == 'OK':
                                pyautogui.typewrite(self.final_text)
                                self.final_text = ''
                                self.camera.mouse_status = MOUSE_MOVING
                                self.can_destroy = True
                            else:
                                self.final_text += button.text
                            sleep(0.15)
            else:
                if time.time() - self._stop_time > self._STOP_DURATION:
                    self._can_action = True
                    self._stop_time = 0

        cv2.imshow("keyboard_image", keyboard_image)
        if self.can_destroy:
            cv2.destroyWindow('keyboard_image')
            self.can_destroy = False
        cv2.waitKey(1)




