from telemetry_f1_2021.listener import TelemetryListener

def GetListenerF12021(port: int = None):
    try:
        return TelemetryListener(port = port)
    except OSError as exception:
        print(f'Unable to setup connection: {exception.args[1]}')
        print('Failed to open connector, stopping.')
        exit(127)

