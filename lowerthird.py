#
# This file is part of Mediary's Caspar Client.
# Copyright (C) 2018 Mediary Limited. All rights reserved.
#

'''
Lower Third widget
'''

import amcp
import colour
import wx
import sys
from configurable import Configurable
import configurable
from widget import Widget

class LowerThird(wx.StaticBox, Widget):
    OPTION_BG='colour_a'
    OPTION_FG='colour_b'

    my_configurations=[configurable.Template,configurable.Layer]
    config_section='lowerthird'
    ui_label='Lower Third'
    my_default_config={'Template': 'mediary/lowerthird', 'Layer': 101}

    def __init__(self, parent, config):
        '''
            Required: parent object, config object
        '''
        super(LowerThird, self).__init__(parent, label=self.ui_label)
        self.parent = parent
        self.config = config

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        if sys.platform=='win32':
            txt = wx.StaticText(self, wx.ID_ANY, '') # seems to be needed on Windows, otherwise stuff smashes the staticbox label
            sizer.Add(txt)

        self.line1 = wx.TextCtrl(self, value='line1')
        sizer.Add(self.line1, flag=wx.EXPAND)
        self.line2 = wx.TextCtrl(self, value='line2')
        sizer.Add(self.line2, flag=wx.EXPAND)

        bFadeOn = wx.Button(self, label='TAKE')
        bFadeOn.Bind(wx.EVT_BUTTON, self.do_fade_on)
        bFadeOff = wx.Button(self, label='OFF')
        bFadeOff.Bind(wx.EVT_BUTTON, self.do_fade_off)
        bUpdate = wx.Button(self, label='Update')
        bUpdate.Bind(wx.EVT_BUTTON, self.do_update)

        inner = wx.BoxSizer(wx.HORIZONTAL)

        self.cp = None # so the immediate callback works
        self.cp = colour.PairedColourPicker(self,
                self.config.get(self.config_section, LowerThird.OPTION_FG, '#ffffff'),
                self.config.get(self.config_section, LowerThird.OPTION_BG, '#eda129'),
                self.got_colours,
                label_patch=' Name ',
                label_inverse=' Title ',
                buttonAlabel='Name text colour', buttonBlabel='Name background colour')
        inner.Add(self.cp, 1, wx.EXPAND)

        inner.AddStretchSpacer(2)

        inner.Add(bFadeOn)
        inner.AddStretchSpacer(1)
        inner.Add(bFadeOff)
        inner.AddStretchSpacer(1)
        inner.Add(bUpdate)


        sizer.AddSpacer(10)
        sizer.Add(inner, flag=wx.EXPAND)
        sizer.AddSpacer(20)

        sizer.AddStretchSpacer()

    def channel(self):
        return self.parent.channel()
    def layer(self):
        return self.config.get_int(self.config_section, configurable.Layer.label, LowerThird.my_default_config[configurable.Layer.label])
    def template(self):
        return self.config.get(self.config_section, configurable.Template.label, LowerThird.my_default_config[configurable.Template.label])

    def fg(self):
        return self.config.get(self.config_section, LowerThird.OPTION_FG, '#ffffff')
    def bg(self):
        return self.config.get(self.config_section, LowerThird.OPTION_BG, '#eda129')

    def templateData(self):
        return amcp.jsondata({
            'name': self.line1.GetValue(),
            'title': self.line2.GetValue(),
            'colourB': self.cp.get_bg(),
            'colourA': self.cp.get_fg(),
            })

    def do_fade_on(self, event):
        # CG channel ADD layer template 1 data
        self.parent.transact('CG %d-%d ADD 1 %s 1 %s'%(self.channel(), self.layer(), amcp.quote(self.template()), self.templateData()))

    def do_fade_off(self, event):
        # CG channel STOP layer
        self.parent.transact('CG %d-%d STOP 1'%(self.channel(), self.layer()))

    def do_update(self,e):
        # CG channel UPDATE layer data
        self.parent.transact('CG %d-%d UPDATE 1 %s'%(self.channel(), self.layer(), self.templateData()))

    def got_colours(self):
        if self.cp:
            self.config.put(self.config_section, LowerThird.OPTION_BG, self.cp.get_bg())
            self.config.put(self.config_section, LowerThird.OPTION_FG, self.cp.get_fg())
            self.config.write()
        self.Refresh()
