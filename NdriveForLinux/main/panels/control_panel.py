#!/usr/bin/env python
# coding=utf-8

import wx
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../components/"))
from wx.lib.buttons import GenBitmapButton
from custom_button import CustomButton as CustomBtn

BITMAP_SELECTIVE_SYNC = os.path.join(os.path.dirname(__file__),
                                     "../../bitmap/selective_sync.png")
BITMAP_SELECTIVE_SYNC_HOVER = os.path.join(os.path.dirname(__file__),
                                     "../../bitmap/selective_sync_hover.png")
BITMAP_ACCOUNT_SETTING = os.path.join(os.path.dirname(__file__),
                                      "../../bitmap/account_setting.png")
BITMAP_STATS = os.path.join(os.path.dirname(__file__),
                            "../../bitmap/stats.png")
BITMAP_DONATION = os.path.join(os.path.dirname(__file__),
                               "../../bitmap/donation.png")

class ControlPanel(wx.Panel):
    def __init__(self, parent):
        super(ControlPanel, self).__init__(parent)
        # Hand cursor.
        if 'phoenix' in wx.PlatformInfo:
            hand_cursor = wx.Cursor(wx.CURSOR_HAND)
        else:
            hand_cursor = wx.StockCursor(wx.CURSOR_HAND)
            
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 'Control Panel' header 
        self.header = wx.StaticText(self, label="제어판",
                                    style=wx.ALIGN_CENTER)
        self.header.SetFont(wx.Font(24, wx.SWISS, wx.NORMAL, wx.BOLD))
        # self.header.SetForegroundColour('#ffffff')
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        header_sizer.Add(self.header, 0, wx.ALIGN_CENTER|wx.ALL, 10)
        
        # Buttons
        icon_size = 32
        
        sizer.Add(header_sizer, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.LEFT|wx.TOP, 20)
        sizer.AddSpacer(20)
        syncImg = wx.Image(BITMAP_SELECTIVE_SYNC).Scale(
            icon_size, icon_size, wx.IMAGE_QUALITY_NEAREST
        )
        syncImg = wx.BitmapFromImage(syncImg)
        syncImg_hover = wx.Image(BITMAP_SELECTIVE_SYNC_HOVER).Scale(
            icon_size, icon_size, wx.IMAGE_QUALITY_NEAREST
        )
        syncImg_hover = wx.BitmapFromImage(syncImg_hover)
        acSettingImg = wx.Image(BITMAP_ACCOUNT_SETTING).Scale(
            icon_size, icon_size, wx.IMAGE_QUALITY_NEAREST
        )
        acSettingImg = wx.BitmapFromImage(acSettingImg)
        statsImg = wx.Image(BITMAP_STATS).Scale(
            icon_size, icon_size, wx.IMAGE_QUALITY_NEAREST
        )
        statsImg = wx.BitmapFromImage(statsImg)
        donateImg = wx.Image(BITMAP_DONATION).Scale(
            icon_size, icon_size, wx.IMAGE_QUALITY_NEAREST
        )
        donateImg = wx.BitmapFromImage(donateImg)
        
        # self.selectiveSyncBtn = GenBitmapButton(self, wx.ID_ANY, syncImg,
        #                                         style=wx.BORDER_NONE)
        # self.acSettingBtn = GenBitmapButton(self, wx.ID_ANY, acSettingImg,
        #                                     style=wx.BORDER_NONE)
        # self.statsBtn = GenBitmapButton(self, wx.ID_ANY, statsImg,
        #                                 style=wx.BORDER_NONE)
        # self.donateBtn = GenBitmapButton(self, wx.ID_ANY, donateImg,
        #                                  style=wx.BORDER_NONE)
        # self.selectiveSyncLabel = wx.StaticText(self, label="동기화 설정",
        #                                         style=wx.ALIGN_CENTER)
        # self.selectiveSyncLabel.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        # 
        # self.acSettingLabel = wx.StaticText(self, label="계정 설정",
        #                                         style=wx.ALIGN_CENTER)
        # self.acSettingLabel.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        # 
        # self.statsLabel = wx.StaticText(self, label="사용량 확인",
        #                                         style=wx.ALIGN_CENTER)
        # self.statsLabel.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        # 
        # self.donateLabel = wx.StaticText(self, label="기부하기",
        #                                         style=wx.ALIGN_CENTER)
        # self.donateLabel.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        self.selectiveSyncBtn = CustomBtn(self, wx.ID_ANY, '동기화 설정')
        normal = (syncImg, 'top')
        focus = (syncImg_hover, 'top')
        self.selectiveSyncBtn.set_bmp(normal, focus)
        self.selectiveSyncBtn.set_border(None)
        self.selectiveSyncBtn.set_bg_color('#dbdbdb')
        self.selectiveSyncBtn.set_cursor(hand_cursor)
        self.selectiveSyncBtn.set_padding( (5, 10, 5, 10) )
        
        self.acSettingBtn = CustomBtn(self, wx.ID_ANY, '계ᅟ정 설정')
        self.acSettingBtn.set_bmp((acSettingImg, 'top'))
        self.acSettingBtn.set_border(None)
        self.acSettingBtn.set_bg_color('#dbdbdb')
        self.acSettingBtn.set_cursor(hand_cursor)
        self.acSettingBtn.set_padding( (5, 10, 5, 10) )
        
        self.statsBtn = CustomBtn(self, wx.ID_ANY, '사용량 확인')
        self.statsBtn.set_bmp((statsImg, 'top'))
        self.statsBtn.set_border(None)
        self.statsBtn.set_bg_color('#dbdbdb')
        self.statsBtn.set_cursor(hand_cursor)
        self.statsBtn.set_padding( (5, 10, 5, 10) )
        
        self.donateBtn = CustomBtn(self, wx.ID_ANY, '응원하기')
        self.donateBtn.set_bmp((donateImg, 'top'))
        self.donateBtn.set_border(None)
        self.donateBtn.set_bg_color('#dbdbdb')
        self.donateBtn.set_cursor(hand_cursor)
        self.donateBtn.set_padding( (5, 10, 5, 10) )

        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.selectiveSyncBtn, 0, wx.ALIGN_CENTER)
        lbl_1 = wx.StaticText(self, label="동기화할 디렉토리파일 혹은 일반파일을 선택합니다",
                              style=wx.ALIGN_CENTER_VERTICAL)
        lbl_1.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))

        
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(self.acSettingBtn, 0, wx.ALIGN_CENTER)
        lbl_2 = wx.StaticText(self, label="어플리케이션에서 사용할 네이버 계정을 설정합니다",
                              style=wx.ALIGN_CENTER_VERTICAL)
        lbl_2.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_3.Add(self.statsBtn, 0, wx.ALIGN_CENTER)
        lbl_3 = wx.StaticText(self, label="현재 남은 클라우드 공간을 확인합니다",
                              style=wx.ALIGN_CENTER_VERTICAL)
        lbl_3.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        sizer_4 = wx.BoxSizer(wx.VERTICAL)
        sizer_4.Add(self.donateBtn, 0, wx.ALIGN_CENTER)
        lbl_4 = wx.StaticText(self, label="프로그램이 마음에 드셨다면,\n가난한 개발자에게 김밥을 선물해주세요",
                              style=wx.ALIGN_CENTER_VERTICAL)
        lbl_4.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
        gs = wx.FlexGridSizer(4, 2, 20, 25)
        gs.AddMany([
            (sizer_3, 0, wx.ALIGN_LEFT|wx.EXPAND), (lbl_3, 0, wx.ALIGN_CENTER_VERTICAL),
            (sizer_1, 0, wx.ALIGN_LEFT|wx.EXPAND), (lbl_1, 0, wx.ALIGN_CENTER_VERTICAL),
            (sizer_2, 0, wx.ALIGN_LEFT|wx.EXPAND), (lbl_2, 0, wx.ALIGN_CENTER_VERTICAL),
            (sizer_4, 0, wx.ALIGN_LEFT|wx.EXPAND), (lbl_4, 0, wx.ALIGN_CENTER_VERTICAL)
        ])
        
        # Position debugging
        print("sizer_1 = " , sizer_1.GetPosition() , "sizer_2 = " , sizer_2.GetPositionTuple())
        
        sizer.Add(gs, 0, wx.ALIGN_CENTER|wx.EXPAND|wx.LEFT, 30)
        self.SetSizer(sizer)
        self.SetBackgroundColour('#dbdbdb')