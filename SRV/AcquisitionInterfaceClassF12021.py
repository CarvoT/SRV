from telemetry_f1_2021.packets import *
import Singleton
from AcquisitionInterfaceClass import AcquisitionInterface, LapData

class AcquisitionInterfaceF12021(AcquisitionInterface):
    
    def slipAngle(self):
        ##3.6m wheelbase of redbull`s F1 car
        if self.speed == 0:
            return 0
        else:
            return (self.steerAngle - ((3.6*self.gForceLateral*9.8)/((self.speed/3.6)^2) )) * 180/3.14

    def steerAngleDeg(self):
        return self.steerAngle * 180/3.14

    def fromPacket(self,packet):
        
        header = PacketHeader.from_buffer_copy(packet)
        if header.m_packet_id == 0:
            packMotion = PacketMotionData.from_buffer_copy(packet)

            self.gForceLateral = packMotion.m_car_motion_data[0].m_g_force_lateral
            self.slipRatio[0] = packMotion.m_wheel_slip[0]
            self.slipRatio[1] = packMotion.m_wheel_slip[1]
            self.slipRatio[2] = packMotion.m_wheel_slip[2]
            self.slipRatio[3] = packMotion.m_wheel_slip[3]
            self.steerAngle = packMotion.m_front_wheels_angle
            self.positionX = packMotion.m_car_motion_data[0].m_world_position_x 
            self.positionY = packMotion.m_car_motion_data[0].m_world_position_y
            self.positionZ = packMotion.m_car_motion_data[0].m_world_position_z

            #test to linefollower args
            self.speedX = packMotion.m_car_motion_data[0].m_world_velocity_x
            self.speedY = packMotion.m_car_motion_data[0].m_world_velocity_y
            self.speedZ = packMotion.m_car_motion_data[0].m_world_velocity_z
            self.yaw = packMotion.m_car_motion_data[0].m_yaw

        if header.m_packet_id == 2:
            packLap = PacketLapData.from_buffer_copy(packet)

            self.lapNo = packLap.m_lap_data[0].m_current_lap_num

        if header.m_packet_id == 6:   
            packTelemetry = PacketCarTelemetryData.from_buffer_copy(packet) 

            self.speed = packTelemetry.m_car_telemetry_data[0].m_speed
            self.gear = packTelemetry.m_car_telemetry_data[0].m_gear
            self.engineRPM = packTelemetry.m_car_telemetry_data[0].m_engine_rpm
            
        if header.m_packet_id == 7:   
            packStatus = PacketCarStatusData.from_buffer_copy(packet) 

            self.maxEngineRPM = packStatus.m_car_status_data[0].m_max_rpm
            self.drs = packStatus.m_car_status_data[0].m_drs_allowed


class LapDataF12021(LapData):
    def newFromPacket(self, packet):
        header = PacketHeader.from_buffer_copy(packet)
        if header.m_packet_id == 0:
            self.data.append(AcquisitionInterfaceF12021())
            self.data[self.maxPos()].copy(self.data[self.maxPos()-1])  
       
        self.data[self.maxPos()].fromPacket(packet)

        if self.data[self.maxPos()].lapNo != self.data[self.maxPos()-1]:
            self.SaveLap()

        self.data[self.maxPos()].id = self.maxPos()

class CurTelemetryF12021(metaclass=Singleton.SingletonInstance):
    
    def __init__(self):
        self.data = AcquisitionInterfaceF12021()