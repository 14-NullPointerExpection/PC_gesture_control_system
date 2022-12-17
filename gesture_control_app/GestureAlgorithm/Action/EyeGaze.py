import cv2
import mediapipe as mp
import time

def draw_point(landmark, image, color=(0, 255, 0), radius=2):
    """绘制人脸关键点"""
    cv2.circle(image, (int(landmark.x * image.shape[1]), int(landmark.y * image.shape[0])), radius, color, -1)

def is_eye_gaze(image):
    mp_face_mesh = mp.solutions.face_mesh # 人脸网格
    with mp_face_mesh.FaceMesh(
        max_num_faces=1, # 最大检测人脸数
        refine_landmarks=True, # 是否精细化人脸关键点
        min_detection_confidence=0.5, # 最小检测置信度
        min_tracking_confidence=0.5) as face_mesh: # 最小跟踪置信度

        image.flags.writeable = False # 可写标志
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # 转换颜色空间
        results = face_mesh.process(image) # 处理图像
                
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:
                
                # 绘制脸部最左和最右的点
                left = face_landmarks.landmark[162]
                right = face_landmarks.landmark[389]
                left1 = face_landmarks.landmark[156]
                right1 = face_landmarks.landmark[383]
                top = face_landmarks.landmark[10]
                bottom = face_landmarks.landmark[152]
                top1 = face_landmarks.landmark[151]
                bottom1 = face_landmarks.landmark[175]
                if (left1.x < left.x) or (right1.x > right.x) or (top1.y < top.y) or (bottom1.y > bottom.y):
                    return False
                else:
                    return True
    return False



def test():
  mp_drawing = mp.solutions.drawing_utils # 绘图工具
  mp_drawing_styles = mp.solutions.drawing_styles # 绘图样式
  mp_face_mesh = mp.solutions.face_mesh # 人脸网格
  drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1) # 绘图规格
  cap = cv2.VideoCapture(0) # 打开摄像头
  
  is_away = False
  
  with mp_face_mesh.FaceMesh(
      max_num_faces=1, # 最大检测人脸数
      refine_landmarks=True, # 是否精细化人脸关键点
      min_detection_confidence=0.5, # 最小检测置信度
      min_tracking_confidence=0.5) as face_mesh: # 最小跟踪置信度
    while cap.isOpened(): # 摄像头打开
      success, image = cap.read() # 读取摄像头数据
      if not success:
        print("Ignoring empty camera frame.")
        # If loading a video, use 'break' instead of 'continue'.
        continue
  
      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False # 可写标志
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # 转换颜色空间
      results = face_mesh.process(image) # 处理图像
  
      # Draw the face mesh annotations on the image.
      image.flags.writeable = True
      image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
      if results.multi_face_landmarks: # 人脸关键点
        for face_landmarks in results.multi_face_landmarks:
          mp_drawing.draw_landmarks(
              image=image,
              landmark_list=face_landmarks,
              connections=mp_face_mesh.FACEMESH_TESSELATION, # 人脸网格
              landmark_drawing_spec=None,
              connection_drawing_spec=mp_drawing_styles
              .get_default_face_mesh_tesselation_style()) # 绘制人脸网格
          mp_drawing.draw_landmarks(
              image=image,
              landmark_list=face_landmarks,
              connections=mp_face_mesh.FACEMESH_CONTOURS, # 人脸轮廓
              landmark_drawing_spec=None,
              connection_drawing_spec=mp_drawing_styles
              .get_default_face_mesh_contours_style()) # 绘制人脸轮廓
          mp_drawing.draw_landmarks(
              image=image,
              landmark_list=face_landmarks,
              connections=mp_face_mesh.FACEMESH_IRISES, # 人脸眼睛
              landmark_drawing_spec=None,
              connection_drawing_spec=mp_drawing_styles
              .get_default_face_mesh_iris_connections_style()) # 绘制人脸眼睛
              
      if results.multi_face_landmarks:
          for face_landmarks in results.multi_face_landmarks:
  
              # 绘制左右眼
  
              left_eye = face_landmarks.landmark[190]
              right_eye = face_landmarks.landmark[414]
              # 蓝色左眼, 粉色右眼
              draw_point(left_eye, image, color=(255, 0, 0), radius=5)
              draw_point(right_eye, image, color=(255, 0, 255), radius=5)
              # print("diff: {}".format(abs(left_eye.x - right_eye.x)))
              
              # 绘制脸部最左和最右的点
              left = face_landmarks.landmark[162]
              right = face_landmarks.landmark[389]
              left1 = face_landmarks.landmark[156]
              right1 = face_landmarks.landmark[383]
              top = face_landmarks.landmark[10]
              bottom = face_landmarks.landmark[152]
              top1 = face_landmarks.landmark[151]
              bottom1 = face_landmarks.landmark[175]
              draw_point(left, image, color=(0, 0, 255), radius=5)
              draw_point(right, image, color=(0, 0, 255), radius=5)
              draw_point(left1, image, color=(255, 0, 255), radius=5)
              draw_point(right1, image, color=(255, 0, 255), radius=5)
              draw_point(top, image, color=(0, 0, 255), radius=5)
              draw_point(bottom, image, color=(0, 0, 255), radius=5)
              draw_point(top1, image, color=(255, 0, 255), radius=5)
              draw_point(bottom1, image, color=(255, 0, 255), radius=5)
              if not is_eye_gaze(image):
                  print("双眼未注视{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
  
              # print("diff_hori: {}, diff_vert: {}".format(abs(left.x - right.x), abs(top.y - bottom.y)))
              face_size_hori = abs(left.x - right.x)
              face_size_vert = abs(top.y - bottom.y)
              is_away_temp = face_size_hori < 0.2 and face_size_vert < 0.3
              if is_away_temp != is_away:
                  is_away = is_away_temp
                  if is_away:
                      print("已离开屏幕:{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                  else:
                      print("已回到屏幕:{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
      # Flip the image horizontally for a selfie-view display.
      cv2.imshow('MediaPipe Face Mesh', cv2.flip(image, 1))
      if cv2.waitKey(5) & 0xFF == 27: # 按下ESC键退出
        break
  cap.release()
