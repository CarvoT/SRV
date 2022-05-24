from DataClass import LapData, CurTelemetry, TelemetryListener
from ControllerClass import Controller
from ThreadsClass import TelemetryThread

from DebugLog import AddDebugLog

import math
import time

class Thread_Telemetry(TelemetryThread):
    def run(self):
        TelemetryListener().close()
        TelemetryListener().setGame(TelemetryListener().getGame(), self.port)

        while not self.killed:
            CurTelemetry().data.fromPacket(TelemetryListener().get())

        TelemetryListener().close()
        
class AutoPilot(object):
    trackingTelemetry = False

    def __init__(self, aTrackingTelemetry):
        self.killed = False
        self.trackingTelemetry = aTrackingTelemetry

    def throttleControl(self, actualSpeed, targetSpeed, slipRatio):
        if targetSpeed > 230:
            targetSpeed = targetSpeed / 0.75 

        if (slipRatio > 0.2) or (slipRatio < -0.2): 
            Controller().Throttle(20) 
        else:
            if actualSpeed + 20 < targetSpeed:
                if actualSpeed > 200:
                    Controller().Throttle(100)
                elif actualSpeed > 180:
                    Controller().Throttle(80)
                elif actualSpeed > 160:
                    Controller().Throttle(70)
                else:
                    Controller().Throttle(60)
            else:
               Controller().Throttle(0)    

    def brakeControl(self, actualSpeed, targetSpeed):
        if targetSpeed > 230:
            targetSpeed = targetSpeed / 0.75

        if actualSpeed > (targetSpeed+10): 
            Controller().Brake(75)
        else:
            Controller().Brake(0)  

    def steerControl(self):
        
        AddDebugLog('------------------------------------------------')

        posX = CurTelemetry().data.positionX
        posZ = CurTelemetry().data.positionZ
        currAngle = math.degrees(float(CurTelemetry().data.yaw))

        AddDebugLog('pos X: ' +  str(posX) + ' pos Z: ' + str(posZ))

        id = LapData().CurId(posX,posZ)

        AddDebugLog('Current id: ' +  str(id))

        if id != -1:
            
            if CurTelemetry().data.speed > 250:
                id = int(id) + 30 
            elif CurTelemetry().data.speed > 200:
                id = int(id) + 15
            elif CurTelemetry().data.speed > 180:
                id = int(id) + 12
            elif CurTelemetry().data.speed > 150:
                id = int(id) + 10
            elif CurTelemetry().data.speed > 100:
                id = int(id) + 8
            elif CurTelemetry().data.speed > 70:
                id = int(id) + 6
            else:
                id = int(id) + 5

            savedTelemetry = LapData().getById(str(id))
            
            AddDebugLog('Target id: ' +  str(id))

            if savedTelemetry:

                difTargetX = float(savedTelemetry.positionX) - posX
                difTargetZ = float(savedTelemetry.positionZ) - posZ
            
                AddDebugLog('target X: ' +  str(savedTelemetry.positionX) + ' target Z: ' + str(savedTelemetry.positionZ))
                AddDebugLog('Dif X: ' +  str(difTargetX) + ' Dif Z: ' + str(difTargetZ))
                AddDebugLog('yaw: ' +  str(currAngle))
            
                if difTargetZ !=0:
                    targetAngle = math.degrees(math.atan(difTargetX/difTargetZ))
            
                AddDebugLog('target Angle: ' +  str(targetAngle))


                if (currAngle > 0):
                    if (currAngle < 90):
                         #1
                        if difTargetZ < 0:                         
                            #troca de quadrante 1 pra 2
                            targetAngle = targetAngle + 180    
                        
                        SteerAngle = currAngle - targetAngle
                    else:
                        #2 
                        if difTargetZ < 0:
                            #troca de quadrante 2 pra 1
                            targetAngle = targetAngle + 180 
                                               
                        SteerAngle = currAngle - targetAngle 
                else:
                    if(currAngle < -90):
                        #3
                        if targetAngle < 0:
                            if difTargetZ > 0:
                                SteerAngle = currAngle - targetAngle
                            elif difTargetX > 0:
                                SteerAngle = currAngle + 180 - targetAngle
                            else:
                                targetAngle = -180 - targetAngle 
                                SteerAngle = targetAngle - currAngle
                        else:
                            targetAngle = targetAngle - 180 
                            SteerAngle = currAngle - targetAngle
                    else:
                        #4 
                        if difTargetZ < 0:
                            #troca de quadrante 4 pra 3 
                            targetAngle = targetAngle -180
                        if (targetAngle > 0) and  (difTargetX < 0):
                            targetAngle = -targetAngle

                        SteerAngle = currAngle - targetAngle

                AddDebugLog('SteerAngle Angle: ' +  str(SteerAngle))
                SteerAngle = SteerAngle * 1.5
                if (CurTelemetry().data.speed > 130) and (CurTelemetry().data.speed < 240): 
                    SteerAngle = SteerAngle * 1.7 
                    
                Controller().Steer(SteerAngle)  

        return id

    def drsControl(self):
        if CurTelemetry().data.drs == 1:
            Controller().ActiveDrs()

    def gearControl(self):
        currSpeed = float(CurTelemetry().data.speed)
        currGear = int(CurTelemetry().data.gear)
        idealGear = 1

        if currSpeed > 290:   
            idealGear = 8
        elif currSpeed > 260: 
            idealGear = 7
        elif currSpeed > 215: 
            idealGear = 6
        elif currSpeed > 170: 
            idealGear = 5
        elif currSpeed > 120: 
            idealGear = 4
        elif currSpeed > 70:  
            idealGear = 3
        elif currSpeed > 30:
            idealGear = 2
        else:
            idealGear = 1

        if currGear > idealGear:
            Controller().GearDown()
        elif currGear < idealGear:
            Controller().GearUp()

    def speedControl(self):
        posX = CurTelemetry().data.positionX
        posZ = CurTelemetry().data.positionZ
        id = LapData().CurId(posX,posZ)
        if id != -1:
            id = int(id) + 20
            savedTelemetry = LapData().getById(str(id))

            if savedTelemetry:
                self.throttleControl(float(CurTelemetry().data.speed), float(savedTelemetry.speed)*0.86, float(CurTelemetry().data.slipRatio[0]))
                self.brakeControl(float(CurTelemetry().data.speed), float(savedTelemetry.speed)*0.86)

    def readLap(self):
        LapData().LoadLap('REF_LAP.txt')

    def startTelemetry(self):
        self.threadTelemetry = Thread_Telemetry()
        if self.trackingTelemetry:
            self.threadTelemetry.setPort(20778)
        else:
            self.threadTelemetry.setPort(20777)
        
        self.threadTelemetry.start()

    def closeTelemetry(self):
        self.threadTelemetry.kill()

    def start(self):
        self.readLap()
        self.startTelemetry()
        
        while not self.killed:

            self.speedControl()
            self.gearControl()
            self.drsControl()
            self.steerControl()

        self.closeTelemetry()
        while self.threadTelemetry.is_alive():
            time.sleep(0.2)

    def kill(self):
        self.killed = True
   