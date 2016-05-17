import wx
import os
from wx.lib.buttons import GenBitmapButton
from wx.lib.buttons import GenBitmapTextButton


BITMAP_HISTORY_IMG = os.path.join(os.path.dirname(__file__), "../../bitmap/history.png")
BITMAP_PROGRESS_IMG = os.path.join(os.path.dirname(__file__), "../../bitmap/progress.png")
BITMAP_INC_SHARE_IMG = os.path.join(os.path.dirname(__file__), "../../bitmap/incoming.png")
BITMAP_ERROR_IMG = os.path.join(os.path.dirname(__file__), "../../bitmap/error.png")

class MenuPanel(wx.Panel):
    def __init__(self, parent):
        super(MenuPanel, self).__init__(parent)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        historyImg = wx.Image(BITMAP_HISTORY_IMG).Scale(
            64, 64,wx.IMAGE_QUALITY_HIGH
        )
        historyImg = wx.BitmapFromImage(historyImg)
        progressImg = wx.Image(BITMAP_PROGRESS_IMG).Scale(
            64, 64,wx.IMAGE_QUALITY_HIGH
        )
        progressImg = wx.BitmapFromImage(progressImg)
        incomeShareImg = wx.Image(BITMAP_INC_SHARE_IMG).Scale(
            64, 64, wx.IMAGE_QUALITY_HIGH
        )
        incomeShareImg = wx.BitmapFromImage(incomeShareImg)
        errorImg = wx.Image(BITMAP_ERROR_IMG).Scale(
            64, 64, wx.IMAGE_QUALITY_HIGH
        )
        errorImg = wx.BitmapFromImage(errorImg)
        
        self.historyButton = GenBitmapTextButton(self, wx.ID_ANY, historyImg,
                                             label="History",
                                             style=wx.BORDER_NONE)
        self.progressButton = GenBitmapButton(self, wx.ID_ANY, progressImg,
                                              style=wx.BORDER_NONE)
        self.incomingButton = GenBitmapButton(self, wx.ID_ANY, incomeShareImg,
                                              style=wx.BORDER_NONE)
        self.errorButton = GenBitmapButton(self, wx.ID_ANY, errorImg,
                                           style=wx.BORDER_NONE)
        self.historyButton.Bind(wx.EVT_BUTTON, self.OnClickHistoryButton)
        self.progressButton.Bind(wx.EVT_BUTTON, self.OnClickProgressButton)
        self.incomingButton.Bind(wx.EVT_BUTTON, self.OnClickIncomingShareButton)
        self.errorButton.Bind(wx.EVT_BUTTON, self.OnClickErrorButton)
        
        sizer.Add(self.historyButton)
        sizer.Add(self.progressButton)
        sizer.Add(self.incomingButton)
        sizer.Add(self.errorButton)
        
        self.SetSizer(sizer)
        self.SetBackgroundColour('#d6d6d6')
        
    def OnClickHistoryButton(self, event):
        print "History"
        
    def OnClickProgressButton(self, event):
        print "Progress"
        
    def OnClickIncomingShareButton(self, event):
        print "Incoming Share"
    
    def OnClickErrorButton(self, event):
        print "Error"
    