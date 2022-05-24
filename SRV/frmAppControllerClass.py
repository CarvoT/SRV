import wx
import time

from ControllerClass import Controller
import LabelsClass

class frmAppController(wx.Frame): 

    def setLabels(self, language):
        if language == 'PT':
            self.labels = LabelsClass.labelsPT()
        else:
            self.labels = LabelsClass.labelsEN()   

    def WaitTime(self):
        try:
            value = float(self.edtWaitTime.GetValue())
        except ValueError:
            value = 0 
        time.sleep(value)

    def EnabledTime(self):
        try:
            value = float(self.edtEnabledTime.GetValue())
        except ValueError:
            value = 0 
        time.sleep(value)
    
    def btnThrottle_click(self, event):
        try:
            value = float(self.edtThrottleValue.GetValue())
        except ValueError:
            Valor = 0 
        self.WaitTime()
        Controller().Throttle(value)
        self.EnabledTime()
        Controller().Throttle(0)

    def btnBrake_click(self, event):
        try:
            value = float(self.edtBrakeValue.GetValue())
        except ValueError:
            value = 0
        self.WaitTime()
        Controller().Brake(value)
        self.EnabledTime()
        Controller().Brake(0)

    def btnSteer_click(self, event):
        try:
            value = float(self.edtSteerValue.GetValue())
        except ValueError:
            value = 0          
        self.WaitTime()
        Controller().Steer(value)
        self.EnabledTime()
        Controller().Steer(0)

    def btnMenu_click(self, event):
        self.WaitTime()
        Controller().PressMenu()

    def btnGearUp_click(self, event):
        self.WaitTime()
        Controller().GearUp()
        
    def btnGearDown_click(self, event):
        self.WaitTime()
        Controller().GearDown()
        
    def btnDrs_click(self, event):
        self.WaitTime()
        Controller().ActiveDrs()

    def CreateForm(self):
        super().__init__(parent=None, title=self.labels.title)
        
        panel = wx.Panel(self)

        #criação dos grupos, utilizados para organização da tela
        grpGeneral = wx.BoxSizer(wx.VERTICAL)   
        grpButtons = wx.BoxSizer(wx.HORIZONTAL)  
        grpButtonsSecondLine = wx.BoxSizer(wx.HORIZONTAL) 
        grpTimes = wx.BoxSizer(wx.HORIZONTAL)  
        grpValues = wx.BoxSizer(wx.HORIZONTAL)  
        
        #edt para escrita
        self.edtThrottleValue = wx.TextCtrl(panel)
        self.edtBrakeValue = wx.TextCtrl(panel)
        self.edtSteerValue = wx.TextCtrl(panel)
        self.edtWaitTime = wx.TextCtrl(panel)
        self.edtEnabledTime = wx.TextCtrl(panel)
        
        #criação das labels
        lblThrottleValue = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER, label = self.labels.lblThrottleValue) 
        lblBrakeValue = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER, label = self.labels.lblBrakeValue) 
        lblSteerValue = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER, label = self.labels.lblSteerValue)
        lblWaitTime = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER, label = self.labels.lblWaitTime)
        lblEnabledTime = wx.StaticText(panel,-1,style = wx.ALIGN_CENTER, label = self.labels.lblEnabledTime) 

        #Grupos de labels
        grpLabelThrottle = wx.BoxSizer(wx.VERTICAL) 
        grpLabelBrake = wx.BoxSizer(wx.VERTICAL) 
        grpLabelSteer = wx.BoxSizer(wx.VERTICAL) 
        grpLabelWaitTime = wx.BoxSizer(wx.VERTICAL) 
        grpLabelEnabledTime= wx.BoxSizer(wx.VERTICAL) 

        #prepara grupo edt label
        grpLabelThrottle.Add(lblThrottleValue, 0, wx.ALL | wx.CENTER, 0) 
        grpLabelThrottle.Add(self.edtThrottleValue, 0, wx.ALL | wx.CENTER, 0) 
        grpLabelBrake.Add(lblBrakeValue, 0, wx.ALL | wx.CENTER, 0)
        grpLabelBrake.Add(self.edtBrakeValue, 0, wx.ALL | wx.CENTER, 0) 
        grpLabelSteer.Add(lblSteerValue, 0, wx.ALL | wx.CENTER, 0) 
        grpLabelSteer.Add(self.edtSteerValue, 0, wx.ALL | wx.CENTER, 0) 
        grpLabelWaitTime.Add(lblWaitTime, 0, wx.ALL | wx.CENTER, 0) 
        grpLabelWaitTime.Add(self.edtWaitTime, 0, wx.ALL | wx.CENTER, 0) 
        grpLabelEnabledTime.Add(lblEnabledTime, 0, wx.ALL | wx.CENTER, 0) 
        grpLabelEnabledTime.Add(self.edtEnabledTime, 0, wx.ALL | wx.CENTER, 0) 

        #criação de botão
        btnThrottle = wx.Button(panel, label=self.labels.btnThrottle)
        btnThrottle.Bind(wx.EVT_BUTTON, self.btnThrottle_click)
        btnBrake = wx.Button(panel, label=self.labels.btnBrake)
        btnBrake.Bind(wx.EVT_BUTTON, self.btnBrake_click)
        btnSteer = wx.Button(panel, label=self.labels.btnSteer)
        btnSteer.Bind(wx.EVT_BUTTON, self.btnSteer_click)
        btnGearUp = wx.Button(panel, label=self.labels.btnGearUp)
        btnGearUp.Bind(wx.EVT_BUTTON, self.btnGearUp_click)
        btnGearDown = wx.Button(panel, label=self.labels.btnGearDown)
        btnGearDown.Bind(wx.EVT_BUTTON, self.btnGearDown_click)
        btnDrs = wx.Button(panel, label=self.labels.btnDrs)
        btnDrs.Bind(wx.EVT_BUTTON, self.btnDrs_click)
        btnMenu = wx.Button(panel, label=self.labels.btnMenu)
        btnMenu.Bind(wx.EVT_BUTTON, self.btnMenu_click)

        #Desenho dos grupos
        panel.SetSizer(grpGeneral)        
        grpGeneral.Add(grpTimes, 0, wx.ALL | wx.CENTER, 0)  
        grpGeneral.Add(grpValues, 0, wx.ALL | wx.CENTER, 0)  
        grpGeneral.Add(grpButtons, 0, wx.ALL | wx.CENTER, 5)  
        grpGeneral.Add(grpButtonsSecondLine, 0, wx.ALL | wx.CENTER, 5)  

        #Desenhos dos edits de tempos
        grpTimes.Add(grpLabelWaitTime, 0, wx.ALL | wx.CENTER, 5)  
        grpTimes.Add(grpLabelEnabledTime, 0, wx.ALL | wx.CENTER, 5)  

        #Desenhos dos edits de valores
        grpValues.Add(grpLabelThrottle, 0, wx.ALL | wx.CENTER, 5)  
        grpValues.Add(grpLabelBrake, 0, wx.ALL | wx.CENTER, 5)  
        grpValues.Add(grpLabelSteer, 0, wx.ALL | wx.CENTER, 5)  
        
        #Desenhos dos botões
        grpButtons.Add(btnThrottle, 0, wx.ALL | wx.CENTER, 5)  
        grpButtons.Add(btnBrake, 0, wx.ALL | wx.CENTER, 5)  
        grpButtons.Add(btnSteer, 0, wx.ALL | wx.CENTER, 5)  
        grpButtonsSecondLine.Add(btnGearUp, 0, wx.ALL | wx.CENTER, 5)  
        grpButtonsSecondLine.Add(btnGearDown, 0, wx.ALL | wx.CENTER, 5)  
        grpButtonsSecondLine.Add(btnDrs, 0, wx.ALL | wx.CENTER, 5)  
        grpButtonsSecondLine.Add(btnMenu, 0, wx.ALL | wx.CENTER, 5) 
        
    def __init__(self):
        
        self.setLabels('PT')
        #self.setBtnLabels('EN')
        self.CreateForm()     
        self.Show()




