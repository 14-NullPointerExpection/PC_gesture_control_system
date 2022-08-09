import time
import pyautogui as pag
import cv2
from cv2 import dnn

import numpy as np
import mediapipe as mp
import _thread

pag.FAILSAFE = False
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(False, min_detection_confidence=0.5, min_tracking_confidence=0.5)


def hand_mask(image, results):
    imgHeight = image.shape[0]
    imgWeight = image.shape[1]
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            pre_x = 0
            pre_y = 0
            x0 = 0
            y0 = 0
            x5 = 0
            y5 = 0
            x17 = 0
            y17 = 0

            for i, lm in enumerate(hand_landmarks.landmark):
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
                cv2.line(image, (x0, y0), (x5, y5), (128, 128, 128), 2)
                cv2.line(image, (x0, y0), (x17, y17), (128, 128, 128), 2)
    return image


def processImg(image):
    x = 0
    y = 0
    black = np.zeros(image.shape, dtype=np.uint8)

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            for i, lm in enumerate(hand_landmarks.landmark):
                if i == 8:
                    x = lm.x
                    y = lm.y

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    black = hand_mask(black, results)

    return black, x, y


def mousemove(x_p, y_p, x_r, y_r):
    x_m = x_r - x_p
    y_m = y_r - y_p

    #print(x_m, y_m)
    if abs(x_m) > 250 or abs(y_m) > 250:
        print("快速移动")
        x_m = int(x_m * 2.5)
        y_m = int(y_m * 2.5)
        pag.moveRel(x_m, y_m, duration=0)
    if abs(x_m) < 100 and abs(y_m) < 100:
        print("慢速移动")
        x_m = int(x_m * 0.5)
        y_m = int(y_m * 0.5)
        pag.moveRel(x_m, y_m, duration=0)
    else:
        x_m = int(x_m * 1.3)
        y_m = int(y_m * 1.3)
        pag.moveRel(x_m, y_m, duration=0)
    return x_r, y_r


def opencamera(model_path):
    # class_name = ['0', '1', '5']
    # net = dnn.readNetFromTensorflow(model_path)
    cap = cv2.VideoCapture(0)

    x_pre = 0
    y_pre = 0
    duration = 0
    pTime = 0
    cTime = 0

    while True:


        _, frame = cap.read()

        src_image = frame


        pic, x, y = processImg(src_image)
        cv2.imshow("pic_p", pic)

        if x != 0 and y != 0:
            x_real = (int(2560 * x))
            y_real = (int(1600 * y))
            print(x_real-x_pre, y_real-y_pre)
            if x_pre - 10 < x_real < x_pre + 10 and y_pre - 10 < y_real < y_pre + 10:
                duration += 1
                print("没动" + str(duration))
                x_pre = x_real
                y_pre = y_real

                if duration >= 10:
                    print("打开")
                    duration = 0
                    print("按下")
                    pag.click()

            else:
                _thread.start_new_thread(mousemove, (x_pre, y_pre, x_real, y_real))
                #mousemove(x_pre, y_pre, x_real, y_real)
                x_pre = x_real
                y_pre = y_real
                duration=0
                # x_pre=x_real
                # y_pre=y_real


                #pag.moveTo((x_real,y_real),duration=0)


            # print(x_real,y_real)
        cTime = time.time()  # 得到当前时间
        fps = 1 / (cTime - pTime)  # 用1除以播放一帧所用时间就可以得出每秒帧数
        pTime = cTime  # 得到这一帧结束时的时间
        cv2.putText(src_image, f"FPS:{int(fps)}", (30, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)  # 将得到的帧数信息打印在图片上

        cv2.imshow("pic", src_image)
        if cv2.waitKey(10) == ord('0'):
            break


opencamera('')
