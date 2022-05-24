import Singleton
from datetime import datetime
import math 


class AcquisitionInterface(object):

    def __init__(self):
        self.id = 0
        self.speed = 0.00
        self.gForceLateral = 0.00
        self.gear = 0
        self.engineRPM = 0
        self.maxEngineRPM = 0
        self.slipRatio = [0]*4
        self.slipAngle = 0.00
        self.steerAngle = 0.00
        self.positionX = 0.00
        self.positionY = 0.00
        self.positionZ = 0.00
        self.lapNo = -1

        #test to linefollower args
        self.speedX = 0.00
        self.speedY = 0.00
        self.speedZ = 0.00
        self.yaw = 0.00

        self.drs = 0

    def copy(self, data):
        self.speed = data.speed
        self.gForceLateral = data.gForceLateral
        self.gear = data.gear
        self.engineRPM = data.engineRPM
        self.maxEngineRPM = data.maxEngineRPM
        self.slipRatio[0] = data.slipRatio[0] 
        self.slipRatio[1] = data.slipRatio[1]
        self.slipRatio[2] = data.slipRatio[2]
        self.slipRatio[3] = data.slipRatio[3]
        self.slipAngle = data.slipAngle
        self.steerAngle = data.steerAngle
        self.positionX = data.positionX
        self.positionY = data.positionY
        self.positionZ = data.positionZ
        self.lapNo = data.lapNo

        #test to linefollower args
        self.speedX = data.speedX
        self.speedY = data.speedY
        self.speedZ = data.speedZ

        self.yaw = data.yaw

        self.drs = data.drs

    def fromPacket(self,packet):
        pass
            
    def toString(self):
        strInterface = ''
        strInterface = strInterface + str(self.id) + '|'
        strInterface = strInterface + str(self.speed) + '|'
        strInterface = strInterface + str(self.gForceLateral)+ '|'
        strInterface = strInterface + str(self.gear) + '|'
        strInterface = strInterface + str(self.engineRPM) + '|'
        strInterface = strInterface + str(self.maxEngineRPM) + '|'
        strInterface = strInterface + str(self.slipRatio[0]) + '|'
        strInterface = strInterface + str(self.slipRatio[1]) + '|'
        strInterface = strInterface + str(self.slipRatio[2]) + '|'
        strInterface = strInterface + str(self.slipRatio[3]) + '|'
        strInterface = strInterface + str(self.slipAngle) + '|'
        strInterface = strInterface + str(self.steerAngle) + '|'
        strInterface = strInterface + str(self.positionX) + '|'
        strInterface = strInterface + str(self.positionY) + '|'
        strInterface = strInterface + str(self.positionZ) + '|'
        strInterface = strInterface + str(self.lapNo)
        
        return strInterface

    def fromString(self, strInterface):
        attributes = strInterface.split("|")
        self.id = attributes[0]
        self.speed = attributes[1]
        self.gForceLateral = attributes[2]
        self.gear = attributes[3]
        self.engineRPM = attributes[4]
        self.maxEngineRPM = attributes[5]
        self.slipRatio[0] = attributes[6]
        self.slipRatio[1] = attributes[7]
        self.slipRatio[2] = attributes[8]
        self.slipRatio[3] = attributes[9]
        self.slipAngle = attributes[10]
        self.steerAngle = attributes[11]
        self.positionX = attributes[12]
        self.positionY = attributes[13]
        self.positionZ = attributes[14]
        self.lapNo = attributes[15]


    
class LapData(metaclass=Singleton.SingletonInstance):
    data = []

    def maxPos(self):
        if self.data:
            return len(self.data) -1
        else:
            return -1

    def __init__(self):
        self.data.append(AcquisitionInterface())
        self.lastSavedLap = -1

    def myPrint(self, index):
        if index == -1:
            index = self.maxPos()

        print(self.data[index].id)
        print(self.data[index].speed)
        print(self.data[index].gForceLateral)
        print(self.data[index].gear)
        print(self.data[index].engineRPM)
        print(self.data[index].maxEngineRPM)
        print(self.data[index].slipRatio[0])
        print(self.data[index].slipRatio[1])
        print(self.data[index].slipRatio[2])
        print(self.data[index].slipRatio[3])
        print(self.data[index].slipAngle)
        print(self.data[index].steerAngle)
        print(self.data[index].positionX)
        print(self.data[index].positionY)
        print(self.data[index].positionZ)
        print(self.data[index].lapNo)

    def SaveLap(self):
        lapToSave = int(self.data[self.maxPos()].lapNo) -1
        
        if lapToSave != self.lastSavedLap:
            file = open(datetime.now().strftime("%m_%d_%Y") + '_Lap_' + str(lapToSave) + '.txt', 'a')
            
            for telemetry in self.data:
                if telemetry.lapNo == lapToSave: 
                    file.write(telemetry.toString())
                    file.write('\n')
            
            self.lastSavedLap = lapToSave
    
    def LoadLap(self, DocName):
        self.data.clear()
        file = open(DocName, 'r')
        for line in file:
            self.data.append(AcquisitionInterface())       
            self.data[self.maxPos()].fromString(line)
        file.close()


    def Goto(self, CurrX, CurrZ, CurrYaw , LastId):

        id = -1
        
        if self.data:

            vecSize = 0.00
            minVecSize = 1.00
            vecSizeReturn = -1.00
            
            for telemetry in self.data:

                if int(telemetry.id) >= int(LastId):

                    compX = float(telemetry.positionX) - CurrX
                    compZ = float(telemetry.positionZ) - CurrZ
                    
                    #yaw 90: X+
                    #yaw -180|180: Z-
                    #yaw 0: Z+ 
                    #yaw -90: X-
                    
                    if (CurrYaw > 0) and (compX < 0):
                        continue
                    if (CurrYaw < 0) and (compX > 0):
                        continue

                    if (CurrYaw < 90) and (CurrYaw > -90):
                        if (compZ < 0):
                            continue
                    else:
                        if (compZ > 0):
                            continue
                    
                    vecSize = math.sqrt(compX**2 + compZ**2)
                
                    if (minVecSize < vecSize) and ((vecSizeReturn == -1.00) or (vecSizeReturn > vecSize)):
                        vecSizeReturn = vecSize
                        id = telemetry.id
                    elif (LastId != -1):
                        break
            
        return id


    def CurId(self, CurrX, CurrZ):

        id = -1
        
        if self.data:
            vecSize = 0.00
            vecSizeReturn = -1.00
            
            for telemetry in self.data:
                compX = float(telemetry.positionX) - CurrX
                compZ = float(telemetry.positionZ) - CurrZ
                    
                vecSize = math.sqrt(compX**2 + compZ**2)
                
                if (vecSizeReturn == -1.00) or (vecSizeReturn > vecSize):
                    vecSizeReturn = vecSize
                    id = telemetry.id            
        return id

    
    def getById(self, id):
        for telemetry in self.data:
            if (telemetry.id == id):
                return telemetry





