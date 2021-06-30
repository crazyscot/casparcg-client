#
# This file is part of Mediary's Caspar Client.
# Copyright (C) 2018 Mediary Limited. All rights reserved.
#

'''
Timer widget
'''

import amcp
import wx
import sys
from configurable import Configurable,FieldValidator,BoolConfigItem
import configurable
from widget import Widget
import datetime

CountMode = configurable.BoolConfigItem('Count up', 'If set, counts upwards. If clear, counts downwards.')
ZeroCut = configurable.BoolConfigItem('Clear on zero', 'Automatically clear the timer when countdown reaches zero?')

def parse_time(f):
    ''' Interprets a user field in format MM:SS or HH:MM:SS '''
    parts=f.split(':')
    if len(parts) not in list(range(2,4)): # i.e. 2 or 3 parts expected
        raise Exception('Clock format must be MM:SS or HH:MM:SS')
    try:
        HH = int(parts[-3])
    except IndexError:
        HH = 0
    MM = int(parts[-2])
    SS = int(parts[-1])
    if SS>60 or HH<0 or MM<0 or SS<0:
        raise Exception('Clock field out of range')
    return datetime.timedelta(0,3600*HH+60*MM+SS,0)

class Timer(wx.StaticBox, Widget):
    my_configurations=[configurable.Template,configurable.Layer, CountMode, ZeroCut]
    config_section='timer'
    ui_label='Timer (clashes with Beneath Score Bug)'
    my_default_config={'Template': 'mediary/timer/countdown_timer', 'Layer': 103, CountMode.label: True, ZeroCut.label: False}

    def __init__(self, parent, config):
        '''
            Required: parent object, config object
        '''
        super(Timer, self).__init__(parent, label=self.ui_label)
        self.parent = parent
        self.config = config

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        if sys.platform=='win32':
            txt = wx.StaticText(self, wx.ID_ANY, '') # seems to be needed on Windows, otherwise stuff smashes the staticbox label
            sizer.Add(txt)

        # First: Timer field

        line1 = wx.BoxSizer(wx.HORIZONTAL)
        bigfont = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.NORMAL)

        self.f_set_time= wx.TextCtrl(self, value='00:00', style=wx.TE_CENTRE,
                validator=configurable.FieldValidator(allowLetters=False, allowColon=True))
        self.f_set_time.SetFont(bigfont)
        line1.AddStretchSpacer(2)
        line1.Add(self.f_set_time, 2, wx.EXPAND)
        line1.AddStretchSpacer(2)

        # Then: Fade On, Fade Off, Update
        line1.AddStretchSpacer(2)
        self.addButton(line1,'TAKE', self.do_anim_on)
        line1.AddStretchSpacer(1)
        self.addButton(line1,'ANIM OFF', self.do_anim_off)
        line1.AddStretchSpacer(1)
        self.addButton(line1,'CUT OFF', self.do_remove)
        line1.AddStretchSpacer(1)

        self.addButton(line1,'Update', self.do_update)
        line1.AddStretchSpacer(2)

        sizer.Add(line1, 0, wx.EXPAND)

        if sys.platform.startswith('linux'):
            sizer.AddSpacer(20) # sigh

    def templateData(self):
        rv = amcp.jsondata({
            'time': self.f_set_time.GetValue(),
            'countUp': self.config.get(self.config_section, CountMode.label),
            'hideOnEnd': self.config.get(self.config_section, ZeroCut.label),
            })
        return rv

    def validate(self):
        try:
            dt = parse_time( self.f_set_time.GetValue() )
        except Exception as e:
            self.parent.blink_status()
            self.parent.status(e.message)
            return False
        return True
