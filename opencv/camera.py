import _thread
import os
import time

import cv2
import pyautogui
from cv2 import dnn
import numpy as np
import mediapipe as mp
import pyautogui as pag
import tensorflow as tf

mp_drawing = mp.solutions.drawing_utils  # 加载手势识别的一些参数
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(False, min_detection_confidence=0.5, min_tracking_confidence=0.5)
pyautogui.FAILSAFE = False


# def binaryMask(frame, x0, y0, width, height):
#     cv2.rectangle(frame, (x0, y0), (x0 + width, y0 + height), (0, 255, 0))
#     roi = frame[y0:y0 + height, x0:x0 + width]
#     # cv2.imshow("roi",roi)#读取roi文件
#     res = skinMask(roi)
#     # cv2.imshow("res",res)
#     return res


# def skinMask(roi):
#     # rgb = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)  # 转换到RGB空间
#     CrCb = cv2.cvtColor(roi, COLOR_BGR2YCrCb)
#     (Y, Cr, Cb) = cv2.split(CrCb)  # 获取图像每个像素点的RGB的值，即将一个二维矩阵拆成三个二维矩阵
#     skin = np.zeros(Cr.shape, dtype=np.uint8)  # 掩膜
#     (x, y) = Cb.shape  # 获取图像的像素点的坐标范围
#     for i in range(0, x):
#         for j in range(0, y):
#             # 判断条件，不在肤色范围内则将掩膜设为黑色，即255
#             # if (abs(R[i][j] - G[i][j]) > 15) and (R[i][j] > G[i][j]) and (R[i][j] > B[i][j]):
#             #     if (R[i][j] > 95) and (G[i][j] > 40) and (B[i][j] > 20) \
#             #             and (max(R[i][j], G[i][j], B[i][j]) - min(R[i][j], G[i][j], B[i][j]) > 15):
#             #         skin[i][j] = 255
#             #     elif (R[i][j] > 220) and (G[i][j] > 210) and (B[i][j] > 170):
#             #         skin[i][j] = 255
#             if (Cr[i][j] > 133) and (Cr[i][j] < 170) and (Cb[i][j] > 77) and (Cb[i][j] < 127):
#                 skin[i][j] = 255
#             else:
#                 skin[i][j] = 0
#     res = cv2.bitwise_and(roi, roi, mask=skin)  # 图像与运算
#
#     kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
#
#     ret1 = cv2.morphologyEx(res, cv2.MORPH_OPEN, kernel, iterations=5)
#
#     return ret1


def hand_mask(image, results):  # 画出手的骨架
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

            for i, lm in enumerate(hand_landmarks.landmark):  # 获取手的坐标点
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


def get_center(image):
    x9 = 0
    y9 = 0
    results = hands.process(image)
    image.flags.writeable = False
    if results.multi_hand_landmarks:
        for hands_landmarks in results.multi_hand_landmarks:
            for i, lm in enumerate(hands_landmarks.landmark):
                if i == 9:
                    x9 = lm.x
                    y9 = lm.y
    image.flags.writeable = True
    return x9, y9


def get_position(image):  # 获取手指的骨架坐标
    # 食指(8)和中指(12)的坐标
    x8 = 0
    y8 = 0
    x12 = 0
    y12 = 0
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    image.flags.writeable = False
    if results.multi_hand_landmarks:
        for hands_landmarks in results.multi_hand_landmarks:
            for i, lm in enumerate(hands_landmarks.landmark):
                if i == 8:
                    x8 = lm.x
                    y8 = lm.y
                if i == 12:
                    x12 = lm.x
                    y12 = lm.y
    image.flags.writeable = True
    black = np.zeros(image.shape, dtype=np.uint8)
    black = hand_mask(black, results)
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_RGB2BGR)
    return black, x8, y8, x12, y12


def process_img(image):  # 图像的预处理
    black = np.zeros(image.shape, dtype=np.uint8)  # 创建一个黑色的图像
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)  # 将图像的颜色空间转换为RGB
    image.flags.writeable = False
    results = hands.process(image)  # 进行手的识别 调用的api
    image.flags.writeable = True

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    black = hand_mask(black, results)

    return black


def move_mouse(x_p, y_p, x_r, y_r):  # 鼠标移动 x_p:手指上一次位置 x_r:手指现在位置
    x_m = x_r - x_p
    y_m = y_r - y_p
    d = 0.1
    if abs(x_m) > 370 or abs(y_m) > 270:
        print("快速移动")
        x_m = int(x_m * 4)
        y_m = int(y_m * 3.5)
        pag.moveRel(x_m, y_m, duration=0.25)
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


def scroll_screen(y_pre, y_real):
    y_m = y_real - y_pre
    print(y_m)
    if abs(y_m) > 500:
        print("滑动")
        if y_m > 0:
            pag.scroll(500)
        else:
            pag.scroll(-500)


def open_camera(model_path):
    class_name = ['1', '2', '5']
    net = dnn.readNetFromTensorflow(model_path)  # 加载模型
    cap = cv2.VideoCapture(1)
    # cap.set(cv2.CAP_PROP_FRAME_COUNT, 1)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    change_mode_pretime = 0
    # change_mode_curtime = 0
    x_pre = 0
    y_pre = 0
    stay_duration = 0
    change_mode_duration = 0
    mode = 0  # 0为移动光标， 1为滚动
    pTime = 0  # 计算帧率
    cTime = 0
    while True:
        _, frame = cap.read()
        src_image = frame
        bone_pic, x8, y8, x12, y12 = get_position(src_image)
        src_image = cv2.flip(src_image, 1)
        cv2.imshow('bone_pic', bone_pic)

        # 控制部分
        if x8 != 0 and y8 != 0:
            x_real = (int(2560 * x8))
            y_real = (int(1600 * y8))
            if mode == 0:
                if x_pre - 10 < x_real < x_pre + 10 and y_pre - 10 < y_real < y_pre + 10:
                    stay_duration += 1
                    print("没动" + str(stay_duration))
                    if abs(x8 - x12) * 2560 < 80 and abs(y8 - y12) * 1600 < 80 and stay_duration > 3:
                        print(abs(x8 - x12), abs(y8 - y12))
                        print("点击")
                        pag.click()
                        stay_duration = 0
                else:
                    # _thread.start_new_thread(move_mouse, (x_pre, y_pre, x_real, y_real))
                    pass

            elif mode == 1:
                scroll_screen(y_pre, y_real)
            x_pre = x_real
            y_pre = y_real
        src_image_y, src_image_x = src_image.shape[:-1]
        center_x, center_y = get_center(src_image)  # 获取中心坐标
        print(center_x, center_y)
        center_x *= src_image_x
        center_y *= src_image_y
        center_x = int(center_x)
        center_y = int(center_y)
        cv2.rectangle(src_image, (center_x, center_y), (center_x + 5, center_y + 5), (0, 0, 255), 1, 4)
        x_left, x_right = int(max(center_x - 150, 0)), int(min(center_x + 150, src_image_x - 1))
        y_left, y_right = int(max(center_y - 150, 0)), int(min(center_y + 150, src_image_y - 1))
        cv2.rectangle(src_image, (x_left, y_left), (x_right, y_right), (0, 255, 0), 1, 4)  # 画出一个矩形框

        pic = frame[100:400, 100:400]  # 截取图像的一部分
        cv2.imshow("pic1", pic)

        pic = cv2.resize(pic, (100, 100))  # 将图像缩放到指定的大小
        pic = process_img(pic)
        cv2.imshow("pic_p", pic)
        blob = cv2.dnn.blobFromImage(pic,
                                     scalefactor=1.0 / 225.,
                                     size=(100, 100),
                                     mean=(0, 0, 0),
                                     swapRB=False,
                                     crop=False)  # 将图像转换为blob格式

        net.setInput(blob)  # 输入图片
        out = net.forward()
        out = out.flatten()

        classId = np.argmax(out)
        print(classId)
        if class_name[classId] == '5' and (time.time() - change_mode_pretime > 10):
            print('-' * 50)
            print(time.time() - change_mode_pretime)
            mode = (1 if mode == 0 else 0)
            print('改变模式为:', mode)
            change_mode_pretime = time.time()
        # print("classId", classId)
        # print("预测结果为：", class_name[classId])

        src_image = cv2.putText(src_image, str(class_name[classId]), (300, 100), cv2.FONT_HERSHEY_SIMPLEX, 2,
                                (0, 0, 255), 2, 4)
        cTime = time.time()  # 得到当前时间
        fps = 1 / (cTime - pTime)  # 用1除以播放一帧所用时间就可以得出每秒帧数
        pTime = cTime  # 得到这一帧结束时的时间
        cv2.putText(src_image, f"FPS:{int(fps)}", (30, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        cv2.imshow("pic", src_image)
        if cv2.waitKey(10) == ord('0'):
            break
