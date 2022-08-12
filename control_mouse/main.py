import time
import pyautogui as pag
import cv2
from cv2 import dnn

import numpy as np
import mediapipe as mp
import _thread

from mediapipe.python.solutions import hands


class ControlMouse:
    is_useful = True
    stop_moving_time = 0
    hands
    def __init__(self):
        pag.FAILSAFE = False
        mp_drawing = mp.solutions.drawing_utils
        mp_hands = mp.solutions.hands
        self.hands = mp_hands.Hands(False,1, min_detection_confidence=0.3, min_tracking_confidence=0.3)

    def processImg(self,image):  # 处理图片
        x8 = 0  # 食指的坐标 是百分比 要乘以屏幕的宽高才得到最终的坐标
        y8 = 0
        x12 = 0
        y12 = 0
        black = np.zeros(image.shape, dtype=np.uint8)

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.hands.process(image)  # 骨架的检测 调的api
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                for i, lm in enumerate(hand_landmarks.landmark):
                    if i == 8:
                        x8 = lm.x
                        y8 = lm.y
                    if i == 12:
                        x12 = lm.x
                        y12 = lm.y

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        black = self.hand_mask(black, results)

        return black, x8, y8, x12, y12

    def opencamera(self):
        # class_name = ['0', '1', '5']
        # net = dnn.readNetFromTensorflow(model_path)
        cap = cv2.VideoCapture(0)
        # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        cap.set(3, 1280)
        cap.set(4, 720)

        x_pre = 0
        y_pre = 0
        duration = 0
        pTime = 0  # 计算帧率的
        cTime = 0

        while True:
            _, frame = cap.read()
            src_image = frame
            pic, x8, y8, x12, y12 = self.processImg(src_image)
            cv2.imshow("pic_p", pic)

            if x8 != 0 and y8 != 0:
                x_real = (int(2560 * x8))
                y_real = (int(1600 * y8))
                if self.is_useful:
                    if x_pre - 10 < x_real < x_pre + 10 and y_pre - 10 < y_real < y_pre + 10:
                        duration += 1
                        print("没动" + str(duration))

                        if abs(x8 - x12) * 2560 < 80 and abs(y8 - y12) * 1600 < 80 and duration > 3:
                            print(abs(x8 - x12), abs(y8 - y12))
                            print("点击")
                            pag.click()
                            duration = 0

                    else:
                        _thread.start_new_thread(self.mousemove, (x_pre, y_pre, x_real, y_real))

                        # _thread.start_new_thread(scrollScreen, (y_pre, y_real))
                        # mousemove(x_pre, y_pre, x_real, y_real)

                        duration = 0
                else:
                    cur_time = time.time()
                    if cur_time - self.stop_moving_time > 0.6:
                        self.is_useful = True

                        self.stop_moving_time = 0
                        print("重新开始运动")
                x_pre = x_real
                y_pre = y_real

                # print(x_real,y_real)
            cTime = time.time()  # 得到当前时间
            fps = 1 / (cTime - pTime)  # 用1除以播放一帧所用时间就可以得出每秒帧数
            pTime = cTime  # 得到这一帧结束时的时间
            cv2.putText(src_image, f"FPS:{int(fps)}", (30, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0),
                        2)  # 将得到的帧数信息打印在图片上

            cv2.imshow("pic", src_image)
            if cv2.waitKey(10) == ord('0'):
                break

    def mousemove(self,x_p, y_p, x_r, y_r):  # 鼠标移动 x_p:手指上一次位置 x_r:手指现在位置
        x_m = x_r - x_p
        y_m = y_r - y_p
        d = 0.1
        if abs(x_m) > 370 or abs(y_m) > 270:

            print("快速移动")
            x_m = int(x_m * 4)
            y_m = int(y_m * 3.5)
            pag.moveRel(x_m, y_m, duration=0.25)

            self.stop_moving_time = time.time()

            self.is_useful = False
        elif abs(x_m) > 210 and abs(y_m) > 170:
            print("中速移动")
            x_m = int(x_m * 3.4)
            y_m = int(y_m * 2.6)
            pag.moveRel(x_m, y_m, duration=d)
        elif abs(x_m) < 150 and abs(y_m) < 120:
            print("慢速移动")
            x_m = int(x_m * 0.7)
            y_m = int(y_m * 0.5)
            pag.moveRel(x_m, y_m, duration=d)
        else:
            x_m = int(x_m * 2.5)
            y_m = int(y_m * 2.0)
            pag.moveRel(x_m, y_m, duration=d)
        return x_r, y_r

    def hand_mask(self,image, results):  # 画出手的骨架
        imgHeight = image.shape[0]
        imgWeight = image.shape[1]
        if results.multi_hand_landmarks:  # 如果有手
            for hand_landmarks in results.multi_hand_landmarks:  # 遍历所有手
                pre_x = 0
                pre_y = 0
                x0 = 0
                y0 = 0
                x5 = 0
                y5 = 0
                x17 = 0
                y17 = 0

                for i, lm in enumerate(hand_landmarks.landmark):  # 遍历所有手的关节点
                    xPos = int(imgWeight * lm.x)  # 将坐标转化为整数
                    yPos = int(imgHeight * lm.y)

                    if i < 5:
                        if pre_x != 0:
                            cv2.line(image, (xPos, yPos), (pre_x, pre_y), (0, 255, 0), 4)  # 大拇指
                            pre_x = xPos
                            pre_y = yPos
                        else:
                            pre_x = xPos
                            pre_y = yPos
                            x0 = xPos
                            y0 = yPos
                    elif 5 <= i <= 8:
                        if i != 5:
                            cv2.line(image, (xPos, yPos), (pre_x, pre_y), (0, 0, 255), 4)  # 食指
                            pre_x = xPos
                            pre_y = yPos
                        else:
                            pre_x = xPos
                            pre_y = yPos
                            x5 = xPos
                            y5 = yPos
                    elif 9 <= i <= 12:
                        if i != 9:
                            cv2.line(image, (xPos, yPos), (pre_x, pre_y), (128, 0, 128), 4)  # 中指
                            pre_x = xPos
                            pre_y = yPos
                        else:
                            pre_x = xPos
                            pre_y = yPos

                    elif 13 <= i <= 16:
                        if i != 13:
                            cv2.line(image, (xPos, yPos), (pre_x, pre_y), (128, 128, 0), 4)  # 无名指
                            pre_x = xPos
                            pre_y = yPos
                        else:
                            pre_x = xPos
                            pre_y = yPos

                    elif 17 <= i <= 20:
                        if i != 17:
                            cv2.line(image, (xPos, yPos), (pre_x, pre_y), (0, 128, 128), 4)  # 小指
                            pre_x = xPos
                            pre_y = yPos
                        else:
                            pre_x = xPos
                            pre_y = yPos
                            x17 = xPos
                            y17 = yPos
                # cv2.circle(image, (xPos, yPos), 3, (255, 0, 0), -1)
                if x0 != 0 and y0 != 0 and x5 != 0 and y5 != 0 and x17 != 0 and y17 != 0:
                    cv2.line(image, (x0, y0), (x5, y5), (128, 128, 128), 2)  # 手掌
                    cv2.line(image, (x0, y0), (x17, y17), (128, 128, 128), 2)  # 手掌
        return image

    def scrollScreen(self,y_pre, y_real):
        y_m = y_real - y_pre
        print(y_m)
        if abs(y_m) > 500:
            print("滑动")
            if y_m > 0:
                pag.scroll(500)
            else:
                pag.scroll(-500)


if __name__ == '__main__':
    c=ControlMouse()
    c.opencamera()
