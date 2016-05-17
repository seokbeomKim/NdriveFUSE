#!/usr/bin/env python
# coding=utf-8
import wx
import os
from wx.lib.buttons import GenBitmapButton

BITMAP_HISTORY_IMG = os.path.join(os.path.dirname(__file__), "../../bitmap/history.png")
BITMAP_PROGRESS_IMG = os.path.join(os.path.dirname(__file__), "../../bitmap/progress.png")
BITMAP_INC_SHARE_IMG = os.path.join(os.path.dirname(__file__), "../../bitmap/incoming.png")
BITMAP_ERROR_IMG = os.path.join(os.path.dirname(__file__), "../../bitmap/error.png")

class MenuPanel(wx.Panel):
    def __init__(self, parent):
        super(MenuPanel, self).__init__(parent)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        icon_size = 32
        historyImg = wx.Image(BITMAP_HISTORY_IMG).Scale(
            icon_size, icon_size,wx.IMAGE_QUALITY_NEAREST
        )
        historyImg = wx.BitmapFromImage(historyImg)
        progressImg = wx.Image(BITMAP_PROGRESS_IMG).Scale(
            icon_size, icon_size,wx.IMAGE_QUALITY_NEAREST
        )
        progressImg = wx.BitmapFromImage(progressImg)
        incomeShareImg = wx.Image(BITMAP_INC_SHARE_IMG).Scale(
            icon_size, icon_size, wx.IMAGE_QUALITY_NEAREST
        )
        incomeShareImg = wx.BitmapFromImage(incomeShareImg)
        errorImg = wx.Image(BITMAP_ERROR_IMG).Scale(
            icon_size, icon_size, wx.IMAGE_QUALITY_NEAREST
        )
        errorImg = wx.BitmapFromImage(errorImg)
        
        self.historyButton = GenBitmapButton(self, wx.ID_ANY, historyImg,
                                             style=wx.BORDER_NONE)
        self.progressButton = GenBitmapButton(self, wx.ID_ANY, progressImg,
                                              style=wx.BORDER_NONE)
        self.incomingButton = GenBitmapButton(self, wx.ID_ANY, incomeShareImg,
                                              style=wx.BORDER_NONE)
        self.errorButton = GenBitmapButton(self, wx.ID_ANY, errorImg,
                                           style=wx.BORDER_NONE)
        
        self.historyLabel = wx.StaticText(self, label="기록",
                                          style=wx.ALIGN_CENTER)
        self.progressLabel = wx.StaticText(self, label="전송",
                                           style=wx.ALIGN_CENTER)
        self.incomingLabel = wx.StaticText(self, label="공유",
                                           style=wx.ALIGN_CENTER)
        self.errorLabel = wx.StaticText(self, label="에러",
                                        style=wx.ALIGN_CENTER)
        
        self.historyLabel.Bind(wx.EVT_COMMAND_LEFT_CLICK, self.OnClickHistoryButton)
        
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.historyButton, 0, wx.LEFT|wx.RIGHT, 10)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.historyLabel)
        
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(self.progressButton, 0, wx.LEFT|wx.RIGHT, 10)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(self.progressLabel)
        
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5.Add(self.incomingButton, 0, wx.LEFT|wx.RIGHT, 10)
        sizer_6 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_6.Add(self.incomingLabel)
        
        sizer_7 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_7.Add(self.errorButton, 0, wx.LEFT|wx.RIGHT, 10)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_8.Add(self.errorLabel)
        
        self.historyButton.Bind(wx.EVT_BUTTON, self.OnClickHistoryButton)
        self.progressButton.Bind(wx.EVT_BUTTON, self.OnClickProgressButton)
        self.incomingButton.Bind(wx.EVT_BUTTON, self.OnClickIncomingShareButton)
        self.errorButton.Bind(wx.EVT_BUTTON, self.OnClickErrorButton)
        
        sizer.AddSpacer(13)
        
        sizer.Add(sizer_1, 0, wx.ALIGN_CENTER|wx.DOWN|wx.UP, 3)
        sizer.Add(sizer_2, 0, wx.ALIGN_CENTER|wx.DOWN, 20)
        sizer.Add(sizer_3, 0, wx.ALIGN_CENTER|wx.ALL, 3)
        sizer.Add(sizer_4, 0, wx.ALIGN_CENTER|wx.DOWN, 20)
        sizer.Add(sizer_5, 0, wx.ALIGN_CENTER|wx.ALL, 3)
        sizer.Add(sizer_6, 0, wx.ALIGN_CENTER|wx.DOWN, 20)
        sizer.Add(sizer_7, 0, wx.ALIGN_CENTER|wx.ALL, 3)
        sizer.Add(sizer_8, 0, wx.ALIGN_CENTER|wx.DOWN, 20)
        
        self.SetSizer(sizer)
        self.SetBackgroundColour('#a0a0a0')
    
        
    def OnClickHistoryButton(self, event):
        print "History"
        
    def OnClickProgressButton(self, event):
        print "Progress"
        
    def OnClickIncomingShareButton(self, event):
        print "Incoming Share"
    
    def OnClickErrorButton(self, event):
        print "Error"
    