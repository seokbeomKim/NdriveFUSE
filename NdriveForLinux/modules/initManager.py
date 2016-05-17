#!/usr/bin/env python
# coding=utf-8

"""
Copyright 2015-2016 Sukbeom Kim

This file is part of NdriveFuse (https://github.com/seokbeomKim/NdriveFUSE/)

NdriveForLinux is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
any later version.

NdriveFUSE is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with NdriveFUSE.  If not, see <http://www.gnu.org/licenses/>.
"""

import wx
import fader
import os
import sys

from os.path import expanduser
import urllib, urllib2
import requests
import simplejson as json
import magic
import datetime
import re
import Cookie 
import cookielib 
import pdb
import time
from ghost import Ghost

import confgen


###############################################################################
"""
Helper class to check user account information
"""
class AccountChecker():
    def __init__(self, NID_AUT = None, NID_SES= None):
        print "Account checker instance is initialized."
        self.session = requests.session()
        self.session.headers["User-Agent"] = \
            "Mozilla/5.0 (Windows NT 6.2; WOW64) Chrome/32.0.1700.76 Safari/537.36"
        self.session.cookies.set('NID_AUT', NID_AUT)
        self.session.cookies.set('NID_SES', NID_SES)
        
    def accountinfo(self, username, password):
        r = self.login(username, password)
        
        return r
    
    def getCookie(self):
        self.ghost = Ghost()
#        pdb.set_trace()
        self.currentPage = None 
        return self.login_try()
    
    def login_try(self):
        print ("user_id = " + self.user_id + ", pw = " + self.password)
        with self.ghost.start() as self.g_session:
            self.g_session.open('https://nid.naver.com/nidlogin.login?svctype=262144&url=http://m.naver.com/')
            self.g_session.evaluate("""
            (function() {        
            document.getElementById('id').value = '%s';
            document.getElementById('pw').value = '%s';
            document.getElementsByClassName('int_jogin')[0].click();
            })();
            """ % (self.user_id, self.password))
            self.g_session.wait_for_selector('#query')
            cookie = {}
            for idx, val in enumerate(self.g_session.cookies):
                key = str(val.name())
                value = str(val.value())
                cookie[key] = value
            return cookie

    def login(self, user_id, password, svctype = "Android NDrive App ver", auth = 0):
        """Log in Naver and get cookie

            >>> s = nd.login("YOUR_ID", "YOUR_PASSWORD")

        :param str user_id: Naver account's login id
        :param str password: Naver account's login password
        :param str svctype: Service type
        :param auth: ???

        :return: ``True`` when success to login or ``False``
        """

        self.user_id = user_id
        self.password = password
        
        if self.user_id == None or self.password == None:
            print "[*] Error __init__: user_id and password is needed"
            return False

        try:
            cookie = self.getCookie()
            return True
        except:
            return False
                    
"""
1st panel: welcome message
"""
class WelcomePanel(wx.Panel):
    def __init__(self, parent):
        super(WelcomePanel, self).__init__(parent)
        
        panel = wx.Panel(self, wx.ID_ANY)
        
        topSizer = wx.BoxSizer(wx.VERTICAL)
        headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        descSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        header = wx.StaticText(self, label="환영합니다")
        desc = wx.StaticText(self, -1,
                             label="비공식 리눅스용 N드라이브 어플리케이션입니다. 진행을 위해 사용자 계정정보를 설정합니다.\n다음 버튼을 눌러 진행해주세요.")
        header.SetFont(wx.Font(40, wx.SWISS, wx.NORMAL, wx.BOLD))
        header.SetSize(header.GetBestSize())
        headerSizer.Add(header,
                        0, wx.ALIGN_CENTER_VERTICAL)
        descSizer.Add(desc,
                      0,wx.ALIGN_CENTER)
        btn = wx.Button(self, wx.ID_OK, label="다음")
        self.Bind(wx.EVT_BUTTON, parent.OnSwitchPanel)
        btnSizer.Add(btn, 0, wx.ALIGN_CENTER)
        
        topSizer.Add(headerSizer, 0, wx.ALIGN_CENTER|wx.UP, 10)
        topSizer.Add(descSizer, 0, wx.ALIGN_CENTER|wx.ALL, 50)
        topSizer.Add(btnSizer, 0, wx.ALIGN_CENTER)
        
        self.SetSizer(topSizer)
        
"""
2nd panel: user account configuration

Read user's account information and check it
"""
class AccountSettingPanel(wx.Panel):
    def __init__(self, parent):
        super(AccountSettingPanel, self).__init__(parent)
        
        textfield_width = 250
        
        panel = wx.Panel(self, wx.ID_ANY)
        
        topSizer = wx.BoxSizer(wx.VERTICAL)
        headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        descSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        wacntSizer = wx.BoxSizer(wx.HORIZONTAL)

        # testing steps
        # step 1. check whether input account is available
        # step 2. encrypt account information
        step1_sizer = wx.BoxSizer(wx.HORIZONTAL)
        step2_sizer = wx.BoxSizer(wx.HORIZONTAL)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        # header and description
        header = wx.StaticText(self, label="계정 설정")
        desc = wx.StaticText(self, -1,
                             label="네이버 N드라이브 사용을 위해 계정정보를 입력하세요. 해당 정보는 로컬에만 저장됩니다.")
        
        header.SetFont(wx.Font(40, wx.SWISS, wx.NORMAL, wx.BOLD))
        header.SetSize(header.GetBestSize())
        headerSizer.Add(header, 0, wx.ALIGN_CENTER_VERTICAL)
        descSizer.Add(desc, 0, wx.ALIGN_CENTER)
        acntSizer = wx.FlexGridSizer(2, 2, 8, 8)
        
        # username
        id_label = wx.StaticText(self, label="아이디")
        self._username = wx.TextCtrl(self, -1, size=(textfield_width, -1))
        acntSizer.Add(id_label, 0, wx.ALIGN_CENTER_VERTICAL)
        acntSizer.Add(self._username, 0,
                      wx.ALIGN_CENTER_VERTICAL)
        # password
        pw_label = wx.StaticText(self, label="비밀번호")
        self._password = wx.TextCtrl(self, -1, size=(textfield_width, -1), style=wx.TE_PASSWORD)
        acntSizer.Add(pw_label, 0, wx.ALIGN_CENTER_VERTICAL)
        acntSizer.Add(self._password, 0,
                      wx.ALIGN_CENTER_VERTICAL)
        
        # step labels
        dlpath = os.path.abspath(os.getcwd())
        iconpath = os.path.join(dlpath, "bitmap/check_icon.png")
        iconbitmap = wx.Bitmap(iconpath, wx.BITMAP_TYPE_PNG)
        iconbitmap.SetSize((16,16))
        self.step1_icon = wx.StaticBitmap(self, bitmap=iconbitmap, size=(16,16))
        self.step2_icon = wx.StaticBitmap(self, bitmap=iconbitmap, size=(16,16))
        self.step1_icon.Hide()
        self.step2_icon.Hide()
        self.step1_label = wx.StaticText(self, label="1. 계정정보 확인")
        self.step2_label = wx.StaticText(self, label="2. 계정정보 암호화 및 저장")
        
        self.step1_label.Hide()
        self.step2_label.Hide()
        
        step1_sizer.Add(self.step1_icon, 0, wx.ALIGN_CENTER_VERTICAL)
        step1_sizer.Add(self.step1_label, 0, wx.ALIGN_CENTER_VERTICAL)
        
        step2_sizer.Add(self.step2_icon, 0, wx.ALIGN_CENTER_VERTICAL)
        step2_sizer.Add(self.step2_label, 0, wx.ALIGN_CENTER_VERTICAL)
        
        # button
        self.btn = wx.Button(self, wx.ID_OK, label="확인",
                             size=(70, 70))
        self.Bind(wx.EVT_BUTTON, parent.OnSwitchPanel)
        btnSizer.Add(self.btn, 0, wx.ALIGN_CENTER)
        
        wacntSizer.Add(acntSizer, 0, wx.ALIGN_CENTER|wx.RIGHT|wx.DOWN, 10)
        wacntSizer.Add(btnSizer, 0, wx.ALIGN_CENTER|wx.DOWN, 10)
        
        # add sizers to top-sizer
        topSizer.Add(headerSizer, 0, wx.ALIGN_CENTER|wx.UP, 10)
        topSizer.Add(descSizer, 0, wx.ALIGN_CENTER|wx.UP|wx.DOWN, 30)
        topSizer.Add(wacntSizer, 0, wx.ALIGN_CENTER|wx.DOWN,10)
        topSizer.Add(step1_sizer, 0, wx.ALIGN_CENTER|wx.ALL, 2)
        topSizer.Add(step2_sizer, 0, wx.ALIGN_CENTER|wx.DOWN, 2)
        
        self.SetSizer(topSizer)

"""
3rd panel: Finish message
"""
class FinishPanel(wx.Panel):
    def __init__(self, parent):
        super(FinishPanel, self).__init__(parent)
        
        panel = wx.Panel(self, wx.ID_ANY)
        
        topSizer = wx.BoxSizer(wx.VERTICAL)
        headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        descSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        header = wx.StaticText(self, label="설정 완료")
        desc = wx.StaticText(self, -1,
                             label="초기설정이 완료되었습니다. 프로그램 아이콘은 노티피케이션 바에서 확인하실 수 있습니다")
        header.SetFont(wx.Font(40, wx.SWISS, wx.NORMAL, wx.BOLD))
        header.SetSize(header.GetBestSize())
        headerSizer.Add(header,
                        0, wx.ALIGN_CENTER_VERTICAL)
        descSizer.Add(desc,
                      0,wx.ALIGN_CENTER)
        btn = wx.Button(self, wx.ID_OK, label="확인")
        self.Bind(wx.EVT_BUTTON, parent.OnSwitchPanel)
        btnSizer.Add(btn, 0, wx.ALIGN_CENTER)
        
        topSizer.Add(headerSizer, 0, wx.ALIGN_CENTER|wx.UP, 10)
        topSizer.Add(descSizer, 0, wx.ALIGN_CENTER|wx.ALL, 50)
        topSizer.Add(btnSizer, 0, wx.ALIGN_CENTER)
        
        self.SetSizer(topSizer)
        
class InitFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="",
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE,
                 name="welcome"):
        super(InitFrame, self).__init__(parent, id, title, pos, size, style, name)
        self.panel = wx.Panel(self)
        
        # setting frame
        x = 0
        y = 0
        size = wx.GetDisplaySize()
        size[0] = size[0] / 2
        size[1] = size[1] / 2
        
        self.SetSize(size)
            
        self.Center()
        
        # panel and layout
        self.welcome_panel = WelcomePanel(self)
        self.accnt_set_panel = AccountSettingPanel(self)
        self.finish_panel = FinishPanel(self)
        self.accnt_set_panel.Hide()
        self.finish_panel.Hide()
        self.panel = self.welcome_panel
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer(1)
        sizer.Add(self.welcome_panel, 0, wx.ALIGN_CENTER|wx.ALL, 12)
        sizer.Add(self.accnt_set_panel, 0, wx.ALIGN_CENTER|wx.ALL, 12)
        sizer.Add(self.finish_panel, 0, wx.ALIGN_CENTER|wx.ALL, 12)
        sizer.AddStretchSpacer(1)
        self.SetSizer(sizer)
        
        self.panel.Layout()
        
    def OnSwitchPanel(self, event):
        print "try to switch panel..."

        if self.welcome_panel.IsShown():
            self.welcome_panel.Hide()
            self.accnt_set_panel.Show()
            self.Layout()
        elif self.accnt_set_panel.IsShown():
            print "Testing account information..."
            checker = AccountChecker()
            
            self.accnt_set_panel.step1_label.Show()
            self.accnt_set_panel.step2_label.Show()
            self.Layout()
            
            # Do step 1
            self.accnt_set_panel.step1_label.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))
            rValue = checker.accountinfo(self.accnt_set_panel._username.GetValue(),
                                         self.accnt_set_panel._password.GetValue())
            if (rValue is False):
                wx.MessageBox("유효하지 않은 계정입니다. 다시 시도해주세요", 'Error', wx.OK | wx.ICON_ERROR)
                self.accnt_set_panel.step1_label.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
                self.accnt_set_panel.step1_label.Hide()
                self.accnt_set_panel.step2_label.Hide()
                self.Layout()
                return
            
            # Do step 2
            self.accnt_set_panel.step1_icon.Show()
            self.accnt_set_panel.step2_label.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL))
            self.Layout()
            
            conf_helper = confgen.ConfGenerator()
            conf_helper.generateFileWithAccntInfo(self.accnt_set_panel._username.GetValue(),
                                                  self.accnt_set_panel._password.GetValue())
            
            self.accnt_set_panel.step2_icon.Show()
            
            # Proceed
            self.accnt_set_panel.Hide()
            self.finish_panel.Show()
            self.Layout()
        elif self.finish_panel.IsShown():
            self.initFlag = True
            self.Close()

# initFlag ... to check whether initialization is succeeded 
InitFrame.initFlag = False

class InitManager(wx.App):
    def OnInit(self):
        print "Init manager is ready."
        return True
    
    def SetCompletedFlag(self, flag):
        self.completedFlag = flag
    
    """
    Check the user's configuration. If new configuration is needed, open the
    new dialog and show interface to user. Otherwise, just skip initialization
    step.
    
    @return True: new config file needed
            False: x
    """
    def checkInitialization(self):
        FILE_PATH = os.getenv('HOME') + "/.ndrivecfg"
        try:
            confFile = open(FILE_PATH, 'r')
        except:
            print "Please make configuration file. See the instruction https://github.com/seokbeomKim/NdriveFUSE"   
            return True
        
        return False
        
    def init(self):
        if self.checkInitialization() == True:
            self.frame = InitFrame(None, title="NDrive client for penguin")
            self.SetTopWindow(self.frame)
            
            self.frame.Show()
        else:
            print "Start main thread for synchronization"
        
