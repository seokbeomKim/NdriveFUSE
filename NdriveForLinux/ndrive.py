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
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))
import initManager
import taskbar

sys.path.append(os.path.join(os.path.dirname(__file__), "main"))
import mainapp

def show_help():
    print "Ndrive for Linux client\n"
    print "Available commands: "
    print "\tstart\t", "Start client and add interface to notification bar"
    print "\tstop\t", "Stop client (sync will be disabled)"

def start():
    print "Start client..."
    initializer = initManager.InitManager()
    initializer.init()
    
    initializer.MainLoop()
    
    if initializer.checkInitialization() == False:
        print "Can Advance.."
        app = mainapp.MainApp()
        tskbarIcon = taskbar.TaskBarIcon()
        tskbarIcon.registerAppReference(app)
        app.MainLoop()
        
    else:
        print "사용자 설정이 필요합니다"
        exit(1)

def reset():
    print "Resetting previous configuration..."
    FILEPATH = os.getenv('HOME') + "/.ndrivecfg"
    os.remove(FILEPATH)

"""
TODO 클라이언트 종료 구현
"""
def stop():
    print "Stopping client..."
    print "Implementation needed."
    
def error(args):
    print "Unknown option: " , args

def main(argc, args):
    if (argc == 1): 
        show_help()
    else:
        if (args[1] == "start"):
            start()
        elif (args[1] == "stop"):
            stop()
        elif (args[1] == "reset"):
            reset()
        else:
            error(args[1])
    
    return 0
        
if __name__ == '__main__':
    main(len(sys.argv), sys.argv)
