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

CountMode = configurable.BoolConfigItem('Count up', 'If set, counts upwards. If clear, counts downwards.')
ZeroCut = configurable.BoolConfigItem('Clear on zero', 'Automatically clear the timer when countdown reaches zero?')

class Timer(wx.StaticBox, Widget):
    my_configurations=[configurable.Template,configurable.Layer, CountMode, ZeroCut]
    config_section='timer'
    ui_label='Timer'
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

        self.f_time= wx.TextCtrl(self, value='00:00:00', style=wx.TE_CENTRE,
                validator=configurable.FieldValidator(allowLetters=False, allowColon=True))
        self.f_time.SetFont(bigfont)
        line1.AddStretchSpacer(2)
        line1.Add(self.f_time, 2, wx.EXPAND)
        line1.AddStretchSpacer(2)

        # Then: Fade On, Fade Off, Update
        line1.AddStretchSpacer(2)
        self.addButton(line1,'Anim on', self.do_anim_on)
        line1.AddStretchSpacer(1)
        self.addButton(line1,'Anim off', self.do_anim_off)
        line1.AddStretchSpacer(1)
        self.addButton(line1,'Update', self.do_update_btn)
        line1.AddStretchSpacer(2)

        sizer.Add(line1, 0, wx.EXPAND)

        if sys.platform.startswith('linux'):
            sizer.AddSpacer(20) # sigh

    def addButton(self, line, label, fn, big=False):
        btn = wx.Button(self, label=label)
        if big: btn.SetFont(self.bigfont)
        btn.Bind(wx.EVT_BUTTON, fn)
        line.Add(btn)
        return btn

    def channel(self):
        return self.parent.channel()
    def layer(self):
        return self.config.get_int(self.config_section, configurable.Layer.label, self.my_default_config[configurable.Layer.label])
    def template(self):
        return self.config.get(self.config_section, configurable.Template.label, self.my_default_config[configurable.Template.label])

    def templateData(self):
        rv = amcp.jsondata({
            'time': self.f_time.GetValue(),
            'countUp': self.config.get(self.config_section, CountMode.label),
            'hideOnEnd': self.config.get(self.config_section, ZeroCut.label),
            })
        return rv

    def do_anim_on(self, event):
        # CG channel ADD layer template 1 data
        self.parent.transact('CG %d-%d ADD 1 %s 1 %s'%(self.channel(), self.layer(), amcp.quote(self.template()), self.templateData()))

    def do_anim_off(self, event):
        # CG channel STOP layer
        self.parent.transact('CG %d-%d STOP 1'%(self.channel(), self.layer()))

    def do_update_btn(self,e):
        self.do_update()

    def do_update(self):
        # CG channel UPDATE layer data
        self.Refresh()
        self.parent.transact('CG %d-%d UPDATE 1 %s'%(self.channel(), self.layer(), self.templateData()))
