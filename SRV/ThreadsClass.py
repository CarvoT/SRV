import threading 


class BaseThread(threading.Thread):
    def __init__(self, *args, **keywords):
        threading.Thread.__init__(self, *args, **keywords)
        self.killed = False
        
    def kill(self):
        self.killed = True


class AppThread(BaseThread):
    def __init__(self, *args, **keywords):
        super().__init__(*args, **keywords)
        self.trackingTelemetry = False

    def setTrackingTelemetry(self, value):
        self.trackingTelemetry = value


class TelemetryThread(BaseThread):

    port = 20778

    def setPort(self, value:int):
        self.port = value
