#
# This file is part of Mediary's Caspar Client.
# Copyright (C) 2018 Mediary Limited. All rights reserved.
#

'''
Widget to put ancillary information (1st qtr, etc.) below the score
bug / next to the timer.
'''

import amcp
import wx
import sys
from configurable import Configurable,FieldValidator,BoolConfigItem
import configurable
from widget import Widget
import datetime

class ScoreExtra(wx.StaticBox, Widget):
    my_configurations=[configurable.Template,configurable.Layer]
    config_section='Score Extra'
    ui_label='Score Extra'
    my_default_config={'Template': 'mediary/scoreextra', 'Layer': 104}

    def __init__(self, parent, config):
        '''
            Required: parent object, config object
        '''
        super(ScoreExtra, self).__init__(parent, label=self.ui_label)
        self.parent = parent
        self.config = config

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        if sys.platform=='win32':
            txt = wx.StaticText(self, wx.ID_ANY, '') # seems to be needed on Windows, otherwise stuff smashes the staticbox label
            sizer.Add(txt)

        line1 = wx.BoxSizer(wx.HORIZONTAL)
        self.text = wx.TextCtrl(self, 2, value='Text Goes Here')
        line1.Add(self.text, 2, flag=wx.EXPAND)

        ###

        # Then: Fade On, Fade Off, Update
        line1.AddStretchSpacer(1)
        self.addButton(line1,'TAKE', self.do_anim_on)
        line1.AddStretchSpacer(1)
        self.addButton(line1,'ANIM OFF', self.do_anim_off)
        line1.AddStretchSpacer(1)
        self.addButton(line1,'CUT OFF', self.do_remove)
        line1.AddStretchSpacer(1)

        self.addButton(line1,'Update', self.do_update)
        #line1.AddStretchSpacer(2)

        sizer.Add(line1, 0, wx.EXPAND)

        if sys.platform.startswith('linux'):
            sizer.AddSpacer(20) # sigh

    def templateData(self):
        rv = amcp.jsondata({
            'line1': str(self.text.GetValue()),
            })
        return rv

if __name__=='__main__':
    import wxclient
    wxclient.run_app([ScoreExtra])
