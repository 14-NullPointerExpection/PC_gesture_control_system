import time

import mediapipe as mp
import cv2
from GestureAlgorithm.Action.BaseAction import BaseAction

from ctypes import *

HWND_BROADCAST = 0xffff
WM_SYSCOMMAND = 0x0112
SC_MONITORPOWER = 0xF170
MonitorPowerOff = 2
SW_SHOW = 5


class FaceAction(BaseAction):
    # 导入人脸识别模块
    _mpFace = mp.solutions.face_detection
    # 自定义人脸识别方法，最小的人脸检测置信度0.5
    _faceDetection = _mpFace.FaceDetection(min_detection_confidence=0.5)
    # 第一次检测到0个人脸的时间
    _zeroTime = 0
    # 每个时间间隔内第一次检测到两个人脸的时间
    _twoTime = 0
    # 警告信号(pyside2前端报警)
    _warningFlag = False
    # 息屏信号
    # _sleepFlag = False
    # 息屏时间间隔
    _sleepDURATION = 10
    # 多人警告时间间隔(单位：秒)
    _warningDURATION = 1
    # 精度阙值
    _ACCURACY = 0.8
    # 总照片数
    _total = 0
    # 两张人脸照片数
    _twoFace = 0

    # 传入Opencv导入的BGR图像，返回人脸数量
    def face_process(self, img):
        # 将每一帧图像传给人脸识别模块
        results = self._faceDetection.process(img)
        # 记录每帧图像中人脸的数量
        faceNum = 0
        # 如果检测不到人脸那就返回None
        if results.detections:
            faceNum = len(results.detections)
        return faceNum

    def screen_off(self):
        windll.user32.PostMessageW(HWND_BROADCAST, WM_SYSCOMMAND,
                                   SC_MONITORPOWER, MonitorPowerOff)

        shell32 = windll.LoadLibrary("shell32.dll")
        shell32.ShellExecuteW(None, 'open', 'rundll32.exe',
                              'USER32,LockWorkStation', '', SW_SHOW)

    def action(self, img):
        faceNum = self.face_process(img)
        self._total += 1
        print("faceNum", faceNum)
        # 检测到没有脸
        if (faceNum == 0):
            # 如果第一次检测到没有脸，那就记录时间
            if (self._zeroTime == 0):
                self._zeroTime = time.time()
            # 如果检测到没有脸的时间超过了阙值，那就息屏
            elif (time.time() - self._zeroTime > self._sleepDURATION):
                # self._sleepFlag = True
                self._zeroTime = 0
                self.screen_off()
                exit()
            return

        # 否则就重置第一次检测到没有脸的时间
        self._zeroTime = 0

        # 检测到两个人脸
        if (faceNum >= 2):
            self._twoFace += 1
            # 如果第一次检测到两个人脸，那就记录时间
            if (self._twoTime == 0):
                self._twoTime = time.time()
            # 如果在时间间隔内检测到两张脸的概率超过阙值，那就报警
            if (time.time() - self._twoTime > self._warningDURATION):
                if (self._twoFace / self._total >= self._ACCURACY):
                    self._warningFlag = True
                    print("警告")
                else:
                    self._warningFlag = False
                # 重置时间和照片数
                self._twoTime = 0
                self._total = 0
                self._twoFace = 0

    def get_warning_flag(self):
        return self._warningFlag

    def set_warning_flag(self, flag):
        self._warningFlag = flag


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    face = FaceAction()
    while True:
        success, img = cap.read()
        face.action(img)
        # cv2.imshow("Image", img)
        cv2.waitKey(10)
