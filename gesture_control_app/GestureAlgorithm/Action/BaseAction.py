class BaseAction:
    def __init__(self):
        # 上一进行该操作的时间点
        self._stop_time = 0
        # 两次该操作之间最小间隔时间
        self._STOP_DURATION = 0.5
        # 是否可以执行动作
        self._can_action = True
