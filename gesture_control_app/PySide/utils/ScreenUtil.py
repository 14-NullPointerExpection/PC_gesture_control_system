# 调节系统屏幕亮度

import wmi

from ctypes import *
SW_SHOW = 5

class ScreenUtil:

    def setBrightness(self, brightness):
        wmi.WMI(namespace='wmi').WmiMonitorBrightnessMethods()[0].WmiSetBrightness(brightness, 0)

    def getBrightness(self):
        return wmi.WMI(namespace='wmi').WmiMonitorBrightness()[0].CurrentBrightness
