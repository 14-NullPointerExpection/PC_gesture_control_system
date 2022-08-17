import cv2
from cvzone.HandTrackingModule import HandDetector
from time import sleep
import numpy as np
import cvzone
from pynput.keyboard import Controller
import mediapipe as mp

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8)
keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]
finalText = ""

keyboard = Controller()
mpHands = mp.solutions.hands#简化函数名
hands = mpHands.Hands(False,4,1,0.7,0.7)#配置侦测过程中的相关参数
mpDraw = mp.solutions.drawing_utils#画点用的函数
handLmStyle = mpDraw.DrawingSpec(color = (0,0,255),thickness = 5)#点的样式，#线的样式BGR，前一个参数是颜色，后一个是粗细
handConStyle = mpDraw.DrawingSpec(color = (0,255,0),thickness = 10)#线的样式BGR，#线的样式BGR，前一个参数是颜色，后一个是粗细


def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img



# def drawAll(img, buttonList):
#     imgNew = np.zeros_like(img, np.uint8)
#     for button in buttonList:
#         x, y = button.pos
#         cvzone.cornerRect(imgNew, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
#                           20, rt=0)
#         cv2.rectangle(imgNew, button.pos, (x + button.size[0], y + button.size[1]),
#                       (255, 0, 255), cv2.FILLED)
#         cv2.putText(imgNew, button.text, (x + 40, y + 60),
#                     cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3)
#
#     out = img.copy()
#     alpha = 0.5
#     mask = imgNew.astype(bool)
#     print(mask.shape)
#     out[mask] = cv2.addWeighted(img, alpha, imgNew, 1 - alpha, 0)[mask]
#     return out


class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

if __name__ == '__main__':
    buttonList = []
    for i in range(len(keys)):
        for j, key in enumerate(keys[i]):
            buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

    while True:
        #____________________
        success, img = cap.read()
        # img = detector.findHands(img)
        img = cv2.cvtColor(cv2.flip(img, 1), cv2.COLOR_BGR2RGB)
        result = hands.process(img)
        lmList=[[0 for _ in range(2)] for _ in range(21)]
        if result.multi_hand_landmarks:
            for handLms in result.multi_hand_landmarks:  # 循环一遍所有的坐标
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS, handLmStyle, handConStyle)  # 画出点和线
                for i, lm in enumerate(handLms.landmark):
                    xPos = int(1280 * lm.x)  # 将坐标转化为整数
                    yPos = int(720 * lm.y)
                    lmList[i][0] = xPos
                    lmList[i][1] = yPos

        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        # lmList, bboxInfo = detector.findPosition(img)
        #_________________________________________
        img = drawAll(img, buttonList)

        if lmList:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size

                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    # l, _, _ = detector.findDistance(8, 12, img, draw=False)
                    l = (pow((lmList[8][0]-lmList[12][0]),2) + pow((lmList[8][1]-lmList[12][1]),2))**0.5
                    print(l)

                    ## when clicked
                    if l < 30:
                        keyboard.press(button.text)
                        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, button.text, (x + 20, y + 65),
                                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                        finalText += button.text
                        sleep(0.15)

        cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
        cv2.putText(img, finalText, (60, 430),
                    cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

        cv2.imshow("Image", img)
        cv2.waitKey(1)