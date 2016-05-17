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
from wx.lib.buttons import GenBitmapButton

print os.getenv('PWD')
BITMAP_LOGO_PATH = os.path.join(os.path.dirname(__file__), "../../bitmap/tray_icon.png")
BITMAP_USER_PATH = os.path.join(os.path.dirname(__file__), "../../bitmap/user_icon.png")

class TopPanel(wx.Panel):
    def __init__(self, parent):
        
        super(TopPanel, self).__init__(parent)
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        logoImg = wx.Image(BITMAP_LOGO_PATH, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        #userImg = wx.Image(BITMAP_USER_PATH, wx.BITMAP_TYPE_PNG).ConvertToBitmap()
        
        # Component initialization
        self.logoButton = GenBitmapButton(self, wx.ID_ANY, logoImg, style=wx.BORDER_NONE)
        self.logoButton.Bind(wx.EVT_BUTTON, self.OnClickLogoButton)
        
        #self.userButton = wx.BitmapButton(self, bitmap=userImg, style=wx.NO_BORDER|wx.BU_EXACTFIT, size=(48,48))        
        #self.userButton.Bind(wx.EVT_BUTTON, self.OnClickUserButton)
        
        
        
        # Pose components above
        sizer.Add(self.logoButton, 0, wx.ALL, 5)
        #sizer.Add(self.userButton, 0, wx.TOP|wx.BOTTOM, 5)
        
        self.SetSizer(sizer)
        self.SetBackgroundColour('#eeeeee')
        
    def OnClickLogoButton(self, event):
        print "Logo Button is clicked.."
        
    def OnClickUserButton(self, event):
        print "User button is clicked..."   
    