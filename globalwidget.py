
'''
Global widget for the client.
Contains ALL OFF and global configuration functions.
'''

import wx

class GlobalWidget(wx.StaticBox):
    def __init__(self, parent):
        '''
            Parent must accept status() calls and have a config member
        '''
        super(GlobalWidget, self).__init__(parent, label='Global')
        self.parent = parent

        bAllOff = wx.Button(self, label='ALL GFX OFF')
        bAllOff.Bind(wx.EVT_BUTTON, self.do_all_off)
        bAllOff.SetBackgroundColour(wx.Colour(255,64,64))

        bConfig = wx.Button(self, label='Configuration')
        bConfig.Bind(wx.EVT_BUTTON, self.do_config)

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(bConfig, 0, wx.ALL, 5)
        sizer.Add((0,0),1) # empty space, expands in proportion
        sizer.AddSpacer(60)
        sizer.Add(bAllOff, 0, wx.ALL, 5)

        self.SetSizer(sizer)

    def do_all_off(self, event):
        self.parent.transact('CLEAR %d'%(self.parent.channel()))

    def do_config(self, event):
        # TODO
        self.parent.status('config nyi')

