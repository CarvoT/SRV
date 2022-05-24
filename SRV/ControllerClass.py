from threading import Thread
import vgamepad as vg
import time
import datetime
import Singleton

class Thread_ActiveDrs(Thread):
    def run(self):
        Controller().oController.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        Controller().oController.update() 
        time.sleep(1)
        Controller().oController.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_Y)
        Controller().oController.update()

class Thread_GearDown(Thread):
    def run(self):
        Controller().oController.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        Controller().oController.update() 
        time.sleep(1)
        Controller().oController.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_LEFT_SHOULDER)
        Controller().oController.update()

class Thread_GearUp(Thread):
    def run(self):
        Controller().oController.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        Controller().oController.update() 
        time.sleep(1)
        Controller().oController.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_RIGHT_SHOULDER)
        Controller().oController.update()

class Thread_PressMenu(Thread):
    def run(self):
        Controller().oController.press_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        Controller().oController.update() 
        time.sleep(1)
        Controller().oController.release_button(button=vg.XUSB_BUTTON.XUSB_GAMEPAD_START)
        Controller().oController.update()


class Controller(metaclass=Singleton.SingletonInstance):
    
    oController = {}
    throttleValue = 0.00
    brakeValue = 0.00
    steerValue = 0.00

    def Connect(self):
        self.oController = vg.VX360Gamepad()
    
    def Correction(self, value, minValue, maxValue):
        if (value > maxValue):
            return maxValue
        elif (value < minValue):
            return minValue
        else:
            return value

    def Throttle(self, percentage):    
        percentage = self.Correction(percentage, 0, 100)
 
        self.throttleValue = percentage * 327.67

        self.oController.right_joystick(x_value=int(self.brakeValue), y_value=int(self.throttleValue))
        self.oController.update() 
        
    def Brake(self, percentage):
        percentage = self.Correction(percentage, 0, 100)

        self.brakeValue = percentage * 327.67

        self.oController.right_joystick(x_value=int(self.brakeValue), y_value=int(self.throttleValue))
        self.oController.update() 

    def SteerCorrection(self, Angle):
        Angle = Angle * 1.9

        map = 70/90
        Angle = (Angle * map)

        if Angle > 1.5:
            Angle = Angle + 30
        elif Angle <-1.5:
            Angle = Angle - 30
        else:
            Angle = 0

        return Angle

    def Steer(self, Angle):
       
        Angle = self.SteerCorrection(Angle)
         
        Angle = self.Correction(Angle, -90, 90)

        multiplier = 32767/90
        self.valueVolante = Angle * multiplier

        self.oController.left_joystick(x_value=int(self.valueVolante), y_value=0)
        self.oController.update() 


    def PressMenu(self):
        Thread_PressMenu().start()

    def GearUp(self):
        Thread_GearUp().start()

    def GearDown(self):
        Thread_GearDown().start()

    def ActiveDrs(self):
        Thread_ActiveDrs().start()

    def Disconnect(self):
        self.oController.__del__() 
