"""
Copyright 2015-2016 Sukbeom Kim

This file is part of NdriveFuse (https://github.com/seokbeomKim/NdriveFUSE/)

NdriveFUSE is free software: you can redistribute it and/or modify
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
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))

TRAY_ICON = os.path.join(os.path.dirname(__file__), "../bitmap/tray_icon.png")
TRAY_TOOLTIP = 'Unofficial N drive client for Linux'

def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item

class TaskBarIcon(wx.TaskBarIcon):
    def __init__(self):
        super(TaskBarIcon, self).__init__()
        
        self.set_icon(TRAY_ICON)
        self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
        self.Bind(wx.EVT_TASKBAR_RIGHT_DOWN, self.on_right_down)
        
        self.popup_menu = self.CreatePopupMenu()

    def CreatePopupMenu(self):
        menu = wx.Menu()
        create_menu_item(menu, 'Open app window', self.open_app_win)
        menu.AppendSeparator()
        create_menu_item(menu, 'Pause syncing', self.pause_sync)
        menu.AppendSeparator()
        create_menu_item(menu, 'Quit', self.on_quit)
        return menu
    
    def registerAppReference(self, ref):
        self.app_ref = ref

    def set_icon(self, path):
        icon = wx.IconFromBitmap(wx.Bitmap(path))
        self.SetIcon(icon, TRAY_TOOLTIP)

    def toggleMainWindow(self):
        if self.app_ref.frame.IsShown():
            self.app_ref.frame.Hide()
        else:
            self.app_ref.frame.Show()
            
    def on_left_down(self, event):
        print 'Tray icon was left-clicked.'
        self.toggleMainWindow()
        
    def on_right_down(self, event):
        print 'Tray icon was right-clicked'
        self.PopupMenu(self.popup_menu)

    def open_app_win(self, event):
        self.toggleMainWindow()
        
    def pause_sync(self, event):
        print 'Pause syncing...'

    def on_quit(self, event):
        print 'Stopping the program...'
        wx.CallAfter(self.Destroy)
        self.app_ref.ExitMainLoop()