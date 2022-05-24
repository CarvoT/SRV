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
        
class lineFollower(object):
    trackingTelemetry = False

    def __init__(self, aTrackingTelemetry):
        self.killed = False
        self.trackingTelemetry = aTrackingTelemetry

    def throttleControl(self, actualSpeed, targetSpeed):        
        if actualSpeed < targetSpeed: 
            Controller().Throttle(60)
        else:
            Controller().Throttle(0)    

    def steerControl(self):        

        AddDebugLog('------------------------------------------------')

        posX = CurTelemetry().data.positionX
        posZ = CurTelemetry().data.positionZ
        currAngle = math.degrees(float(CurTelemetry().data.yaw))
        
        AddDebugLog('pos X: ' +  str(posX) + ' pos Z: ' + str(posZ))
        
        id = LapData().CurId(posX,posZ)

        AddDebugLog('Current id: ' +  str(id))

        if id != -1:
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

                Controller().Steer(SteerAngle)  

        return id

    def speedControl(self): 
        self.throttleControl(CurTelemetry().data.speed, 70)


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
            idd = self.steerControl()

        self.closeTelemetry()
        
        while self.threadTelemetry.is_alive():
            time.sleep(0.2)

    def kill(self):
        self.killed = True
   