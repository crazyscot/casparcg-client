#!/usr/bin/env python2

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
from lowerthird import LowerThird

class LowerThirdBanner(wx.StaticBox, Widget):
    my_configurations=[configurable.Template,configurable.Layer]
    config_section='lowerthird_banner'
    ui_label='Lower Third Banner'
    my_default_config={'Template': 'mediary/lt_banner', 'Layer': 101}

    def __init__(self, parent, config):
        '''
            Required: parent object, config object
        '''
        super(LowerThirdBanner, self).__init__(parent, label=self.ui_label)
        self.parent = parent
        self.config = config

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        if sys.platform=='win32':
            txt = wx.StaticText(self, wx.ID_ANY, '') # seems to be needed on Windows, otherwise stuff smashes the staticbox label
            sizer.Add(txt)

        self.line1 = wx.TextCtrl(self, value='')
        sizer.Add(self.line1, flag=wx.EXPAND)
        ## horiz sizer
        l2s = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(l2s, flag=wx.EXPAND)
        self.line2_l = wx.TextCtrl(self, 1, value='')
        l2s.Add(self.line2_l, 1)
        self.line2_c = wx.TextCtrl(self, 1, value='')
        l2s.Add(self.line2_c, 1)
        self.line2_r = wx.TextCtrl(self, 1, value='')
        l2s.Add(self.line2_r, 1)

        bFadeOn = wx.Button(self, label='TAKE')
        bFadeOn.Bind(wx.EVT_BUTTON, self.do_anim_on)
        bFadeOff = wx.Button(self, label='ANIM OFF')
        bFadeOff.Bind(wx.EVT_BUTTON, self.do_anim_off)
        bCutOff = wx.Button(self, label='CUT OFF')
        bCutOff.Bind(wx.EVT_BUTTON, self.do_remove)
        bUpdate = wx.Button(self, label='Update')
        bUpdate.Bind(wx.EVT_BUTTON, self.do_update)

        inner = wx.BoxSizer(wx.HORIZONTAL)

        self.cp = None # so the immediate callback works
        self.cp = colour.PairedColourPicker(self,
                self.config.get(self.config_section, LowerThird.OPTION_FG, '#ffffff'),
                self.config.get(self.config_section, LowerThird.OPTION_BG, '#eda129'),
                self.got_colours,
                label_patch=' Line1 ',
                label_inverse=' Line2 ',
                buttonAlabel='Line1 text colour', buttonBlabel='Line1 background colour')
        inner.Add(self.cp, 1, wx.EXPAND)

        inner.AddStretchSpacer(2)

        inner.Add(bFadeOn)
        inner.AddStretchSpacer(1)
        inner.Add(bFadeOff)
        inner.AddStretchSpacer(1)
        inner.Add(bCutOff)
        inner.AddStretchSpacer(1)
        inner.Add(bUpdate)


        sizer.AddSpacer(10)
        sizer.Add(inner, flag=wx.EXPAND)
        sizer.AddSpacer(20)

        sizer.AddStretchSpacer()

    def fg(self):
        return self.config.get(self.config_section, LowerThird.OPTION_FG, '#ffffff')
    def bg(self):
        return self.config.get(self.config_section, LowerThird.OPTION_BG, '#eda129')

    def templateData(self):
        return amcp.jsondata({
            'line1': self.line1.GetValue(),
            'line2_l': self.line2_l.GetValue(),
            'line2_c': self.line2_c.GetValue(),
            'line2_r': self.line2_r.GetValue(),
            'colourB': self.cp.get_bg(),
            'colourA': self.cp.get_fg(),
            })

    def got_colours(self):
        if self.cp:
            self.config.put(self.config_section, LowerThird.OPTION_BG, self.cp.get_bg())
            self.config.put(self.config_section, LowerThird.OPTION_FG, self.cp.get_fg())
            self.config.write()
        self.Refresh()

if __name__=='__main__':
    import wxclient
    wxclient.run_app([LowerThirdBanner])
