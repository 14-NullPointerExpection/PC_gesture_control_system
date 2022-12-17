import mediapipe as mp
import cv2
import time

# 导入人脸识别模块
mpFace = mp.solutions.face_detection
# 导入绘图模块
mpDraw = mp.solutions.drawing_utils
# 自定义人脸识别方法，最小的人脸检测置信度0.5
faceDetection = mpFace.FaceDetection(min_detection_confidence=0.5)

# 传入Opencv导入的BGR图像，返回人脸数量
def face_process(img):
    global pTime
    # 将每一帧图像传给人脸识别模块
    results = faceDetection.process(img)

    faceNum = 0  # 记录每帧图像中人脸的数量

    # 如果检测不到人脸那就返回None
    if results.detections:

        faceNum = len(results.detections)

    return faceNum


def main():
    # 从摄像头读取视频
    cap = cv2.VideoCapture(0)

    # 处理每一帧图像
    while True:

        # 每次取出一帧图像，返回是否读取成功(True/False)，以及读取的图像数据
        success, img = cap.read()

        if not success:
            print("Ignoring empty camera frame.")
            continue

        print(face_process(img))

        if cv2.waitKey(50) & 0xFF == 27:  # 每帧滞留50毫秒后消失，ESC键退出
            break

    # 释放视频资源
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
