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
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__) + "/panels"))
from top_panel import TopPanel
from menu_panel import MenuPanel
from control_panel import ControlPanel

sys.path.append(os.path.join(os.path.dirname(__file__) + "../modules"))

import threading
from helper import Helper 

"""
DEFAULT VALUES
"""
WIDTH = 530
HEIGHT = 600

MOUNTPOINT = os.path.join(os.getenv('HOME') + "/ndrive")


class MainApp(wx.App):
    def OnInit(self):
        print "MainApp intialized"
        self.init()
        return True
    
    def init(self):
        # Before we initialize layout, prepare helper instances
        Helper.ConfManager.readConfFile()
        account = Helper.ConfManager.getAccountInfo()
        print account[0], account[1]
        # obj = NDriveFUSE.NDriveFUSE(MOUNTPOINT, account[0], account[1], self.ConfManager)

        # Run FUSE
        # FUSE(obj, MOUNTPOINT, nothreads=False, foreground=False)
        
        # Layout
        self.frame = MainFrame(None, title="NDrive client for penguin", size=(WIDTH, HEIGHT))
        self.SetTopWindow(self.frame)
    
        self.frame.CenterOnScreen()
        # Hide main frame
        self.frame.Hide()
    

class MainFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="",
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER | wx.NO_BORDER,
                 name=""):
        super(MainFrame, self).__init__(parent, id, title, pos, size, style, name)

        print "main frame"
        
        # initialize layout
        self.initLayout()
        
    """
    Organize layout
    """
    def initLayout(self):
        self.setTopLayout()
        self.setMidLeftLayout()
        self.setMidRightLayout()
        self.setBottomLayout()
        
        # After prepare each panel, layout those panels within sizer
        
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.topPanel, 0, wx.EXPAND|wx.ALIGN_CENTER)
        self.midSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.midSizer.Add(self.menuPanel, 0, wx.EXPAND, 10)
        self.midSizer.Add(self.controlPanel, 1, wx.EXPAND, 12)
        self.sizer.Add(self.midSizer, 1, wx.EXPAND, 0)
        #self.sizer.Add(self.bottomPanel, 0, wx.ALIGN_CENTER|wx.ALL, 12)
        
        self.SetSizer(self.sizer)
    
        self.Layout()
    """
    Setting layout
    """
    def setTopLayout(self):
        self.topPanel = TopPanel(self)
    
    def setMidLeftLayout(self):
        self.menuPanel = MenuPanel(self)
    
    def setMidRightLayout(self):
        self.controlPanel = ControlPanel(self)
        pass
    
    def setBottomLayout(self):
        #self.bottomPanel = BottomPanel(self)
        pass
    