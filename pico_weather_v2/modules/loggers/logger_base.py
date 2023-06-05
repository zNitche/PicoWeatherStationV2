import machine


class LoggerBase:
    def __init__(self):
        self.logs_timer = machine.Timer()

    def init_timer(self, periodic, period):
        mode = machine.Timer.ONE_SHOT if not periodic else machine.Timer.PERIODIC
        self.logs_timer.init(period=period, mode=mode, callback=lambda t: self.timer_callback())

    def timer_callback(self):
        pass
