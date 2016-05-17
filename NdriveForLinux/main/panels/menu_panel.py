#!/usr/bin/env python
# coding=utf-8
import wx
import os
from wx.lib.buttons import GenBitmapButton, GenButton
import wx.lib.platebtn as PlateButton

BITMAP_HISTORY_IMG = os.path.join(os.path.dirname(__file__), "../../bitmap/history.png")
BITMAP_PROGRESS_IMG = os.path.join(os.path.dirname(__file__), "../../bitmap/progress.png")
BITMAP_INC_SHARE_IMG = os.path.join(os.path.dirname(__file__), "../../bitmap/incoming.png")
BITMAP_ERROR_IMG = os.path.join(os.path.dirname(__file__), "../../bitmap/error.png")

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../components/"))

from custom_button import CustomButton as CustomBtn

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
        
        # Hand cursor.
        if 'phoenix' in wx.PlatformInfo:
            hand_cursor = wx.Cursor(wx.CURSOR_HAND)
        else:
            hand_cursor = wx.StockCursor(wx.CURSOR_HAND)
        
        # self.historyButton = GenBitmapButton(self, wx.ID_ANY, historyImg,
        #                                      style=wx.BORDER_NONE)
        # self.progressButton = GenBitmapButton(self, wx.ID_ANY, progressImg,
        #                                       style=wx.BORDER_NONE)
        # self.incomingButton = GenBitmapButton(self, wx.ID_ANY, incomeShareImg,
        #                                       style=wx.BORDER_NONE)
        # self.errorButton = GenBitmapButton(self, wx.ID_ANY, errorImg,
        #                                    style=wx.BORDER_NONE)
        # 
        # self.historyLabel = wx.StaticText(self, label="기록",
        #                                   style=wx.ALIGN_CENTER)
        # self.historyLabel.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        # 
        # self.progressLabel = wx.StaticText(self, label="전송",
        #                                    style=wx.ALIGN_CENTER)
        # self.progressLabel.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        # self.incomingLabel = wx.StaticText(self, label="공유",
        #                                    style=wx.ALIGN_CENTER)
        # self.incomingLabel.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        # self.errorLabel = wx.StaticText(self, label="에러",
        #                                 style=wx.ALIGN_CENTER)
        # self.errorLabel.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        self.historyButton = CustomBtn(self, wx.ID_ANY, '기록')
        self.historyButton.set_bmp((historyImg, 'top'))
        self.historyButton.set_border(None)
        self.historyButton.set_bg_color('#a0a0a0')
        self.historyButton.set_cursor(hand_cursor)
        self.historyButton.set_padding( (5, 10, 5, 10) )

        self.progressButton = CustomBtn(self, wx.ID_ANY, '전ᅟ송')
        self.progressButton.set_bmp((progressImg, 'top'))
        self.progressButton.set_border(None)
        self.progressButton.set_bg_color('#a0a0a0')
        self.progressButton.set_cursor(hand_cursor)
        
        self.incomingButton = CustomBtn(self, wx.ID_ANY, '공유')
        self.incomingButton.set_bmp((incomeShareImg, 'top'))
        self.incomingButton.set_border(None)
        self.incomingButton.set_bg_color('#a0a0a0')
        self.incomingButton.set_cursor(hand_cursor)
        
        self.errorButton = CustomBtn(self, wx.ID_ANY, '에러')
        self.errorButton.set_bmp((errorImg, 'top'))
        self.errorButton.set_border(None)
        self.errorButton.set_bg_color('#a0a0a0')
        self.errorButton.set_cursor(hand_cursor)
        
        sizer_1 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.historyButton, 0, wx.LEFT|wx.RIGHT, 10)
        
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2.Add(self.progressButton, 0, wx.LEFT|wx.RIGHT, 10)
        
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_3.Add(self.incomingButton, 0, wx.LEFT|wx.RIGHT, 10)

        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(self.errorButton, 0, wx.LEFT|wx.RIGHT, 10)
        
        self.historyButton.Bind(wx.EVT_BUTTON, self.OnClickHistoryButton)
        self.progressButton.Bind(wx.EVT_BUTTON, self.OnClickProgressButton)
        self.incomingButton.Bind(wx.EVT_BUTTON, self.OnClickIncomingShareButton)
        self.errorButton.Bind(wx.EVT_BUTTON, self.OnClickErrorButton)
        
        sizer.AddSpacer(13)
        
        # '기ᅟ록' 버ᅟ튼
        sizer.Add(sizer_1, 0, wx.ALIGN_CENTER|wx.DOWN|wx.UP, 20)
        sizer.Add(sizer_2, 0, wx.ALIGN_CENTER|wx.DOWN|wx.UP, 20)
        sizer.Add(sizer_3, 0, wx.ALIGN_CENTER|wx.DOWN|wx.UP, 20)
        sizer.Add(sizer_4, 0, wx.ALIGN_CENTER|wx.DOWN|wx.UP, 20)
        
        
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
    