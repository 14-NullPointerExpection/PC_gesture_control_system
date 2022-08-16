class Action:
    def __init__(self):
        # 应该停止移动的时间点
        self._stop_time = 0
        # 停止移动的持续时间
        self._STOP_DURATION = 0.5
        # 是否可以移动
        self._can_action = True
