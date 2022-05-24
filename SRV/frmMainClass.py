
import wx
from ControllerClass import Controller
import time

from frmAppControllerClass import frmAppController
from DataClass import LapData, TelemetryListener, StartDataClass
import LineFollowerClass
import AutoPilotClass
import LabelsClass
from ThreadsClass import AppThread

class Thread_RecordLap(AppThread):

    def run(self):
        TelemetryListener().close()
        if self.trackingTelemetry:
            TelemetryListener().setGame(TelemetryListener().getGame(), 20778)
        else:
            TelemetryListener().setGame(TelemetryListener().getGame(), 20777)

        while not self.killed:
            LapData().newFromPacket(TelemetryListener().get())
            
        TelemetryListener().close()

class Thread_AutoDrive_v1(AppThread):

    def run(self):
        self.lineFollower = LineFollowerClass.lineFollower(self.trackingTelemetry)
        self.lineFollower.start()

    def kill(self):
        super().kill()
        self.lineFollower.kill()

class Thread_AutoDrive_v2(AppThread):

    def run(self):
        self.autoPilot = AutoPilotClass.AutoPilot(self.trackingTelemetry)
        self.autoPilot.start()

    def kill(self):
        super().kill()
        self.autoPilot.kill()
        

class frmMain(wx.Frame):

    def setBtnLabels(self, language):
        if language == 'PT':
            self.labels = LabelsClass.labelsPT()
        else:
            self.labels = LabelsClass.labelsEN()    

    def btnControllerCalibration_click(self, event):                
        app = wx.App()
        frame = frmAppController()

        app.MainLoop()

    def btnRecordLap_click(self, event):
        if self.inRecLap:
            self.inRecLap = False
            self.threadRecordLap.kill()
            while self.threadRecordLap.is_alive():
                time.sleep(0.2)
            self.btnRecordLap.SetLabel(self.labels.btnRecordLap)
        else:
            self.inRecLap = True
            self.threadRecordLap = Thread_RecordLap()
            self.threadRecordLap.setTrackingTelemetry(self.chkTrackingTelemetry.IsChecked())
            self.threadRecordLap.start()
            self.btnRecordLap.SetLabel(self.labels.btnCancel)
        

    def btnAutoDriveV1_click(self, event):
        if self.inAutoDrive:
            self.inAutoDrive = False
            self.threadLine.kill()
            while self.threadLine.is_alive():
                time.sleep(0.2)
            self.btnAutoDriveV1.SetLabel(self.labels.btnAutoDriveV1)
        else:
            self.inAutoDrive = True
            self.threadLine = Thread_AutoDrive_v1()
            self.threadLine.setTrackingTelemetry(self.chkTrackingTelemetry.IsChecked())
            self.threadLine.start()
            self.btnAutoDriveV1.SetLabel(self.labels.btnCancel)

    def btnAutoDriveV2_click(self, event):
        if self.inAutoDrive:
            self.inAutoDrive = False
            self.threadLine.kill()
            while self.threadLine.is_alive():
                time.sleep(0.2)
            self.btnAutoDriveV2.SetLabel(self.labels.btnAutoPilotV2)
        else:
            self.inAutoDrive = True
            self.threadLine = Thread_AutoDrive_v2()
            self.threadLine.setTrackingTelemetry(self.chkTrackingTelemetry.IsChecked())
            self.threadLine.start()
            self.btnAutoDriveV2.SetLabel(self.labels.btnCancel)

    def ConnectController(self):
        Controller().Connect()
            
    def btnReconnectController_click(self, event):
        self.ConnectController()

    def CreateForm(self):
        super().__init__(parent=None, title='SRV - F1 2021')
        
        panel = wx.Panel(self)

        grpGeral = wx.BoxSizer(wx.VERTICAL)  

        self.btnControllerCalibration = wx.Button(panel, label=self.labels.btnControllerCalibration)
        self.btnControllerCalibration.Bind(wx.EVT_BUTTON, self.btnControllerCalibration_click)
        self.btnRecordLap = wx.Button(panel, label=self.labels.btnRecordLap)
        self.btnRecordLap.Bind(wx.EVT_BUTTON, self.btnRecordLap_click)
        self.btnAutoDriveV1 = wx.Button(panel, label=self.labels.btnAutoDriveV1)
        self.btnAutoDriveV1.Bind(wx.EVT_BUTTON, self.btnAutoDriveV1_click)
        self.btnAutoDriveV2 = wx.Button(panel, label=self.labels.btnAutoPilotV2)
        self.btnAutoDriveV2.Bind(wx.EVT_BUTTON, self.btnAutoDriveV2_click)
        self.btnReconnectController = wx.Button(panel, label=self.labels.btnReconnectController)
        self.btnReconnectController.Bind(wx.EVT_BUTTON, self.btnReconnectController_click)
        self.chkTrackingTelemetry = wx.CheckBox(panel, label=self.labels.chkTrackingTelemetry)
        self.chkTrackingTelemetry.SetValue(True)

        panel.SetSizer(grpGeral)        
        grpGeral.Add(self.chkTrackingTelemetry, 0, wx.ALL | wx.CENTER, 5) 
        grpGeral.Add(self.btnAutoDriveV2, 0, wx.ALL | wx.CENTER, 5)  
        grpGeral.Add(self.btnAutoDriveV1, 0, wx.ALL | wx.CENTER, 5) 
        grpGeral.Add(self.btnRecordLap, 0, wx.ALL | wx.CENTER, 5)  
        grpGeral.Add(self.btnControllerCalibration, 0, wx.ALL | wx.CENTER, 5) 
        grpGeral.Add(self.btnReconnectController, 0, wx.ALL | wx.CENTER, 5)

    def __init__(self):
        self.inAutoDrive = False
        self.inRecLap = False

        StartDataClass('F1 2021', 20777)
        
        self.setBtnLabels('PT')
        #self.setBtnLabels('EN')

        self.CreateForm()        
        self.ConnectController()
        self.Show()