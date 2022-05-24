from datetime import datetime

def AddDebugLog(strLog):
    if False:
        file = open(datetime.now().strftime("%m_%d_%Y") + '_Log.txt', 'a')
        file.write('[' + datetime.now().strftime("%H:%M:%S") + '] - ' + strLog)
        file.write('\n')

        print(strLog)
            