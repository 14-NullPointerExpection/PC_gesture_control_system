import sys
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from GestureAlgorithm import camera
from GestureAlgorithm.camera import Camera


class CameraThread(QThread):
    def __init__(self, cam, ):
        super().__init__()
        self.cam = cam

    def run(self):
        camera.start(self.cam)

    # 终止线程
    def stop(self):
        self
        self.quit()
        self.wait()


class WarningWindow(QWidget):
    def __init__(self, cls):
        super(WarningWindow, self).__init__()
        self.cls = cls
        self.cb = QCheckBox("不再提醒")
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText("生人警告！！\n检测到背后有人靠近!!")
        self.msg.setWindowTitle("警告")
        self.msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.msg.setDefaultButton(QMessageBox.Yes)
        self.msg.setCheckBox(self.cb)
        # 设置最高优先级
        self.msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        with open(
                'D:\\WorkSpace\\PycharmProjects\\PC_gesture_control_system\\gesture_control_app\\PySide\\resources\\qss\\WarningMessage.qss',
                'r', encoding='UTF-8') as f:
            self.msg.setStyleSheet(f.read())
        self.timeId = self.startTimer(100)

    def warning(self):
        reply = self.msg.exec()
        if reply == QMessageBox.Yes:
            if self.cb.isChecked():
                self.killTimer(self.timeId)


    def timerEvent(self, event) -> None:
        if (self.cls.face_detection.get_warning_flag()):
            self.warning()
            self.cls.face_detection.set_warning_flag(False)
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WarningWindow()
    sys.exit(app.exec_())
