
'''
Global widget for the client.
Contains ALL OFF and global configuration functions.
'''

import wx
import sys

class GlobalWidget(wx.StaticBox):
    def __init__(self, parent):
        '''
            Parent must accept status() calls and have a config member
        '''
        super(GlobalWidget, self).__init__(parent, label='Global')
        self.parent = parent

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        if sys.platform=='win32':
            txt = wx.StaticText(self, wx.ID_ANY, '') # seems to be needed on Windows, otherwise stuff smashes the staticbox label
            sizer.Add(txt)

        bConfig = wx.Button(self, label='Configuration')
        bConfig.Bind(wx.EVT_BUTTON, self.do_config)

        bAllOff = wx.Button(self, label='ALL GFX OFF')
        bAllOff.Bind(wx.EVT_BUTTON, self.do_all_off)
        bAllOff.SetBackgroundColour(wx.Colour(255,64,64))
        inner = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(inner, flag=wx.EXPAND)
        inner.Add(bConfig)
        inner.AddStretchSpacer()
        inner.Add(bAllOff)

        if sys.platform.startswith('linux'):
            sizer.AddSpacer(20) # sigh

    def do_all_off(self, event):
        self.parent.transact('CLEAR %d'%(self.parent.channel()))

    def do_config(self, event):
        # TODO
        self.parent.status('config nyi')

