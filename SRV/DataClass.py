import Singleton


from AcquisitionInterfaceClassF12021 import LapDataF12021, CurTelemetryF12021
from ListenerF12021 import GetListenerF12021

class CurTelemetryConnector(metaclass=Singleton.SingletonInstance):
    Object = {}

    def setGame(self, game):
        if game == 'F1 2021':
            self.Object = CurTelemetryF12021()

class LapDataConnector(metaclass=Singleton.SingletonInstance):
    Object = []

    def setGame(self, game):
        if game == 'F1 2021':
            self.Object = LapDataF12021()

class TelemetryListener(metaclass=Singleton.SingletonInstance):
    currentGame = ''
    connector = {}

    def getGame(self):
        return self.currentGame

    def setGame(self, game, port):
        self.currentGame = game

        if self.currentGame == 'F1 2021':
            self.connector = GetListenerF12021(port)


    def get(self):
        return self.connector.get()

    def close(self):
        if self.currentGame == 'F1 2021':
            self.connector.socket.close()


def StartDataClass(game, port):
    TelemetryListener().setGame(game, port)
    LapDataConnector().setGame(game)
    CurTelemetryConnector().setGame(game)

def CurTelemetry():
    return CurTelemetryConnector().Object

def LapData():
    return LapDataConnector().Object