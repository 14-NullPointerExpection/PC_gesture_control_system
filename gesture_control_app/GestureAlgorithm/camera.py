"""
author: GYH
desc: 实现摄像头图像识别的相关操作
"""
import time

import cv2 as cv
import numpy as np
from cv2 import dnn
import mediapipe as mp
import _thread
from Action import mouseMoving, ScrollScreen

# 定义模式对应的常量
MOUSE_CONTROL_MODE = 0
SHORTCUTS_MODE = 1
# 定义鼠标状态对应的变量
MOUSE_MOVING = 0
SCROLL_SCREEN = 1


class Camera:
    def __init__(self, model_path, class_names, mode):

        # 加载模型
        self.model = dnn.readNetFromTensorflow(model_path)
        # 设置类别名
        self.class_names = class_names
        # 设置摄像头
        self.capture = cv.VideoCapture(0)
        self.capture.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
        self.capture.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
        # 设置手势识别
        self.hands = mp.solutions.hands.Hands(False, min_detection_confidence=0.3, min_tracking_confidence=0.3)
        # 关键坐标点（原始）
        self.points = []
        self.mode = mode
        self.mouse_status = 0
        # 记录开始改变状态的时间
        self.change_begin_time = 0
        # 需要保持该手势持续的时间,以改变状态
        self.keep_time = 3
        self.mouse_moving = mouseMoving.MouseMoving()
        self.scroll_screen = ScrollScreen.ScrollScreen()

    # 通过摄像头捕获一帧图像，并进行翻转操作
    def get_frame_image(self):
        is_success, frame = self.capture.read()
        if is_success:
            frame = cv.flip(frame, 1)
            return frame

    # 传入一张图像，获取图像中的关键点
    def get_critical_hands_points(self, image):
        points = []
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        results = self.hands.process(image)
        if results.multi_hand_landmarks:
            for hands_landmarks in results.multi_hand_landmarks:
                for i, landmark in enumerate(hands_landmarks.landmark):
                    points.append((landmark.x, landmark.y))
                break
        self.points = points
        return points

    # 根据传入的关键点，使用OpenCV绘制骨架图
    def get_bone_image(self, image):
        points = self.points
        height = image.shape[0]
        width = image.shape[1]
        black_image = np.zeros(image.shape, dtype=np.uint8)
        if len(points):
            # 将点映射到真实图片的位置
            points = list(map(lambda p: (int(p[0] * width), int(p[1] * height)), points))
            for i in range(0, 4):
                cv.line(black_image, (points[i][0], points[i][1]), (points[i + 1][0], points[i + 1][1]), (0, 255, 0), 4)
            for i in range(5, 8):
                cv.line(black_image, (points[i][0], points[i][1]), (points[i + 1][0], points[i + 1][1]), (0, 0, 255), 4)
            for i in range(9, 12):
                cv.line(black_image, (points[i][0], points[i][1]), (points[i + 1][0], points[i + 1][1]), (128, 0, 128),
                        4)
            for i in range(13, 16):
                cv.line(black_image, (points[i][0], points[i][1]), (points[i + 1][0], points[i + 1][1]), (128, 128, 0),
                        4)
            for i in range(17, 20):
                cv.line(black_image, (points[i][0], points[i][1]), (points[i + 1][0], points[i + 1][1]), (0, 128, 128),
                        4)
            cv.line(black_image, (points[0][0], points[0][1]), (points[0 + 1][0], points[0 + 1][1]), (128, 128, 128), 4)
            cv.line(black_image, (points[5][0], points[5][1]), (points[0][0], points[0][1]), (128, 128, 128), 4)
            cv.line(black_image, (points[17][0], points[17][1]), (points[0][0], points[0][1]), (128, 128, 128), 4)
        return black_image

    # 根据骨架图和获取的关键点，获取感兴趣的区域
    def get_roi(self, image):
        points = self.points
        image_height, image_width = image.shape[0], image.shape[1]

        # 获取中心点坐标
        center_x, center_y = points[9]
        center_x *= image_width
        center_y *= image_height
        center_x = int(center_x)
        center_y = int(center_y)
        x_left, x_right = int(max(center_x - 200, 0)), int(min(center_x + 200, image_width - 1))
        y_top, y_bottom = int(max(center_y - 200, 0)), int(min(center_y + 200, image_height - 1))
        # 截取图片
        pic = image[y_top:y_bottom, x_left:x_right]
        return pic

    # 使用神经网络对处理好的图片进行分类操作
    def categorize_image(self, image):
        # 调整图像大小
        image_resized = cv.resize(image, (100, 100))
        # 将图像转换为blob格式
        image_blob = dnn.blobFromImage(image_resized,
                                       scalefactor=1.0 / 225.,
                                       size=(100, 100),
                                       mean=(0, 0, 0),
                                       swapRB=False,
                                       crop=False)
        net = self.model
        net.setInput(image_blob)
        # 得到预测结果
        result = net.forward()
        result = result.flatten()
        class_id = np.argmax(result)
        return self.class_names[class_id]

    # 切换当前的鼠标操控模式
    def change_mouse_status(self, class_id):
        if class_id == '5':
            # 如果开始的时间为0,就赋上现在的时间为初值
            if self.change_begin_time == 0:
                self.change_begin_time = time.time()
            else:
                # 如果保持的时间超过需要的时间,就改变状态
                if time.time() - self.change_begin_time > self.keep_time:
                    self.mouse_status = self.mouse_status ^ 1
                    print('change')
                    self.change_begin_time = 0
        else:
            self.change_begin_time = 0

    # 根据传入的分类，执行某些操作
    def execute_action(self,points):

        # 鼠标模式的操作
        if self.mode == MOUSE_CONTROL_MODE:
            if self.mouse_status == MOUSE_MOVING:
                action = self.mouse_moving
                print("kaishyidong1")
                action.action(points)
            elif self.mouse_status == SCROLL_SCREEN:
                action = self.scroll_screen
                action.action(points)
        # 快捷指令模式
        elif self.mode == SHORTCUTS_MODE:
            pass

    # 手势识别全操作，包括获取关键点，获取感兴趣的区域
    def gesture_recognition(self, image):
        critical_points = self.get_critical_hands_points(image)

        if len(critical_points):
            # 识别出骨架图
            bone_image = self.get_bone_image(image)
            #cv.imshow('bone', bone_image)
            # 截取手部的ROI
            roi_image = self.get_roi(bone_image)
            # 送入神经网络进行识别
            class_id = self.categorize_image(roi_image)
            # 根据识别的结果判断模式的切换与否
            self.change_mouse_status(class_id)


if __name__ == '__main__':
    camera = Camera('../125.pb', class_names=['1','2','5'], mode=MOUSE_CONTROL_MODE)
    while True:
        pic = camera.get_frame_image()
        camera.gesture_recognition(pic)
        if len(camera.points):
            camera.execute_action(camera.points,)

