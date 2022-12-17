import mediapipe as mp
import cv2
import time

# 导入人脸识别模块
mpFace = mp.solutions.face_detection
# 导入绘图模块
mpDraw = mp.solutions.drawing_utils
# 自定义人脸识别方法，最小的人脸检测置信度0.5
faceDetection = mpFace.FaceDetection(min_detection_confidence=0.5)

pTime = 0  # 记录每帧图像处理的起始时间

boxlist = []  # 保存每帧图像每个框的信息


# 传入Opencv导入的BGR图像，返回人脸数量
def face_process(img):
    global pTime
    # 将每一帧图像传给人脸识别模块
    results = faceDetection.process(img)

    faceNum = 0  # 记录每帧图像中人脸的数量

    # 如果检测不到人脸那就返回None
    if results.detections:
        # 返回人脸索引index(第几张脸)，和关键点的坐标信息
        for index, detection in enumerate(results.detections):
            # 遍历每一帧图像并打印结果
            # print(index, detection)
            # 每帧图像返回一次是人脸的几率，以及识别框的xywh，后续返回关键点的xy坐标
            # print(detection.score)  # 是人脸的的可能性
            # print(detection.location_data.relative_bounding_box)  # 识别框的xywh

            # 设置一个边界框，接收所有的框的xywh及关键点信息
            bboxC = detection.location_data.relative_bounding_box

            # 接收每一帧图像的宽、高、通道数
            ih, iw, ic = img.shape

            # 将边界框的坐标点从比例坐标转换成像素坐标
            # 将边界框的宽和高从比例长度转换为像素长度
            bbox = (int(bboxC.xmin * iw), int(bboxC.ymin * ih),
                    int(bboxC.width * iw), int(bboxC.height * ih))

            # 有了识别框的xywh就可以在每一帧图像上把框画出来
            # cv2.rectangle(img, bbox, (255,0,0), 5)  # 自定义绘制函数，不适用官方的mpDraw.draw_detection

            # 把人脸的概率显示在检测框上,img画板，概率值*100保留两位小数变成百分数，再变成字符串
            cv2.putText(img, f'{str(round(detection.score[0] * 100, 2))}%',
                        (bbox[0], bbox[1] - 20),  # 文本显示的位置，-20是为了不和框重合
                        cv2.FONT_HERSHEY_PLAIN,  # 文本字体类型
                        2, (0, 0, 255), 2)  # 字体大小; 字体颜色; 线条粗细

            # 保存索引，人脸概率，识别框的x/y/w/h
            boxlist.append([index, detection.score, bbox])

            # （3）修改识别框样式
            x, y, w, h = bbox  # 获取识别框的信息,xy为左上角坐标点
            x1, y1 = x + w, y + h  # 右下角坐标点

            # 绘制比矩形框粗的线段，img画板，线段起始点坐标，线段颜色，线宽为8
            cv2.line(img, (x, y), (x + 20, y), (255, 0, 255), 4)
            cv2.line(img, (x, y), (x, y + 20), (255, 0, 255), 4)

            cv2.line(img, (x1, y1), (x1 - 20, y1), (255, 0, 255), 4)
            cv2.line(img, (x1, y1), (x1, y1 - 20), (255, 0, 255), 4)

            cv2.line(img, (x1, y), (x1 - 20, y), (255, 0, 255), 4)
            cv2.line(img, (x1, y), (x1, y + 20), (255, 0, 255), 4)

            cv2.line(img, (x, y1), (x + 20, y1), (255, 0, 255), 4)
            cv2.line(img, (x, y1), (x, y1 - 20), (255, 0, 255), 4)

            # 在每一帧图像上绘制矩形框
            cv2.rectangle(img, bbox, (255, 0, 255), 1)  # 自定义绘制函数
        faceNum = len(results.detections)

    # 记录每帧图像处理所花的时间
    cTime = time.time()
    fps = 1 / (cTime - pTime)  # 计算fps值
    pTime = cTime  # 更新每张图像处理的初始时间

    # 把fps值显示在图像上,img画板;fps变成字符串;显示的位置;设置字体;字体大小;字体颜色;线条粗细
    cv2.putText(img, f'FPS: {str(int(fps))}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

    # 显示图像，输入窗口名及图像数据
    cv2.imshow('image', img)

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

        # 将opencv导入的BGR图像转为RGB图像
        # imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        print(face_process(img))

        if cv2.waitKey(50) & 0xFF == 27:  # 每帧滞留50毫秒后消失，ESC键退出
            break

    # 释放视频资源
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
