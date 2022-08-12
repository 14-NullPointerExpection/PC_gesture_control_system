import random

import cv2
import os
import numpy as np
import mediapipe as mp
import camera
from os import listdir


def processingPic(file_pathname, file_pathname_new):  # 处理数据集图片
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(True, 1, min_detection_confidence=0.3, min_tracking_confidence=0.3)
    # 遍历该目录下的所有图片文件
    for filename in os.listdir(file_pathname):
        n = file_pathname + '\\' + filename
        pt = print(n)
        for f in os.listdir(n):
            image = cv2.imread(n + '/' + f)

            # image = cv2.resize(image, (100, 100))

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            results = hands.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            black = np.zeros(image.shape, dtype=np.uint8)

            black = camera.hand_mask(black, results)

            print(file_pathname_new + "\\" + filename + '\\' + f)
            cv2.imwrite(file_pathname_new + "\\" + filename + '\\' + f, black)


def removeBlack(file_pathname):  # 删除黑色图片
    count = 0

    for filename in os.listdir(file_pathname):
        n = file_pathname + '\\' + filename
        pt = print(n)
        for f in os.listdir(n):

            image = cv2.imread(n + '/' + f)

            black = np.zeros(image.shape, dtype=np.uint8)

            difference = cv2.subtract(image, black)
            result = not np.any(difference)

            if result is True:
                print("全黑" + file_pathname + "\\" + filename + '\\' + f)
                os.remove(file_pathname + "\\" + filename + '\\' + f)
                count += 1
    print("共删除" + str(count) + "张图片")


def getTestData(file_pathname, file_pathname_new):  # 获取测试数据
    for filename in os.listdir(file_pathname):
        n = file_pathname + '\\' + filename
        count = 0

        for f in os.listdir(n):
            t = random.randint(0, 6)
            if t == 0:
                image = cv2.imread(n + '/' + f)
                print(file_pathname_new + "\\" + filename + '\\' + f)
                cv2.imwrite(file_pathname_new + "\\" + filename + '\\' + f, image)
                count += 1
        print(filename + "共抽取" + str(count) + "张图片")
