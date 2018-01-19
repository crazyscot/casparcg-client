#
# This file is part of Mediary's Caspar Client.
# Copyright (C) 2018 Mediary Limited. All rights reserved.
#

'''
Score Bug widget
'''

import amcp
import colour
import wx
import sys
from configurable import Configurable,FieldValidator,IntConfigItem
import configurable
from widget import Widget

ITEM_TEAM1='team1'
ITEM_TEAM2='team2'
ITEM_FG1='team1fg'
ITEM_BG1='team1bg'
ITEM_FG2='team2fg'
ITEM_BG2='team2bg'

class FontSize(IntConfigItem):
    label='Font size'
    helptext='Font size in pixels'

class ScoreBug(wx.StaticBox, Widget):
    my_configurations=[configurable.Template,configurable.Layer, FontSize]
    config_section='scorebug'
    ui_label='Score bug'
    my_default_config={'Template': 'mediary/scorebug', 'Layer': 20, FontSize.label: 24}

    def __init__(self, parent, config):
        '''
            Required: parent object, config object
        '''
        super(ScoreBug, self).__init__(parent, label=self.ui_label)
        self.parent = parent
        self.config = config

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        if sys.platform=='win32':
            txt = wx.StaticText(self, wx.ID_ANY, '') # seems to be needed on Windows, otherwise stuff smashes the staticbox label
            sizer.Add(txt)

        # First line: Team names and scores

        line1 = wx.BoxSizer(wx.HORIZONTAL)
        bigfont = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        team1 = self.config.get(self.config_section, ITEM_TEAM1, 'AAA')
        self.team1ctrl = wx.TextCtrl(self, 2, value = team1)
        self.team1ctrl.SetFont(bigfont)
        line1.Add(self.team1ctrl, 1)
        self.score1 = 0
        self.score1ctrl = wx.TextCtrl(self, 1, value='', validator=FieldValidator(allowLetters=False))
        self.score1ctrl.SetFont(bigfont)
        line1.Add(self.score1ctrl, 1)

        line1.AddStretchSpacer(1)

        team2 = self.config.get(self.config_section, ITEM_TEAM2, 'BBB')
        self.team2ctrl = wx.TextCtrl(self, value = team2)
        self.team2ctrl.SetFont(bigfont)
        line1.Add(self.team2ctrl, 1)
        self.score2 = 0
        self.score2ctrl = wx.TextCtrl(self, 1, value='', validator=FieldValidator(allowLetters=False))
        self.score2ctrl.SetFont(bigfont)
        line1.Add(self.score2ctrl, 1)

        self.update_display()
        sizer.Add(line1, 0, wx.EXPAND)

        # Second line: +1, -1, Update, +1, -1
        line2 = wx.BoxSizer(wx.HORIZONTAL)
        lineX = line2
        def addButton(label, fn, big=False):
            btn = wx.Button(self, label=label)
            if big: btn.SetFont(bigfont)
            btn.Bind(wx.EVT_BUTTON, fn)
            lineX.Add(btn)
            return btn
        addButton('+1', self.team1plus1, True)
        line2.AddSpacer(10)
        addButton('-1', self.team1minus1)
        line2.AddStretchSpacer(1)
        line2.AddSpacer(10)
        addButton('+1', self.team2plus1, True)
        line2.AddSpacer(10)
        addButton('-1', self.team2minus1)
        sizer.AddStretchSpacer(1)
        sizer.AddSpacer(10)
        sizer.Add(line2, 0, wx.EXPAND)

        # Third line: Colour 1, Fade On, Fade Off, Update, Colour 2
        line3 = wx.BoxSizer(wx.HORIZONTAL)

        self.team1cp = self.team2cp = None
        self.team1cp = colour.PairedColourPicker(self,
                self.config.get(self.config_section, ITEM_FG1, '#ffffff'),
                self.config.get(self.config_section, ITEM_BG1, '#0000ff'),
                self.got_colours, sample_patch=False)
        line3.Add(self.team1cp, 1, wx.EXPAND)

        line3.AddStretchSpacer(2)

        lineX = line3
        addButton('Fade on', self.do_fade_on)
        line3.AddSpacer(10)
        addButton('Fade off', self.do_fade_off)
        line3.AddSpacer(10)
        addButton('Update', self.do_update_btn)

        line3.AddStretchSpacer(2)

        self.team2cp = colour.PairedColourPicker(self,
                self.config.get(self.config_section, ITEM_FG2, '#ffffff'),
                self.config.get(self.config_section, ITEM_BG2, '#008000'),
                self.got_colours, sample_patch=False)
        line3.Add(self.team2cp, 1, wx.EXPAND)

        sizer.AddStretchSpacer()
        sizer.AddSpacer(10)
        sizer.Add(line3, 0, wx.EXPAND)
        self.update_field_colours()

        if sys.platform.startswith('linux'):
            sizer.AddSpacer(20) # sigh


    def update_display(self):
        self.score1ctrl.SetValue(str(self.score1))
        self.score2ctrl.SetValue(str(self.score2))

    def channel(self):
        return self.parent.channel()
    def layer(self):
        return self.config.get_int(self.config_section, configurable.Layer.label, 1)
    def template(self):
        return self.config.get(self.config_section, configurable.Template.label, 'lowerthird')

    def templateData(self):
        rv = amcp.jsondata({
            'team1': str(self.team1ctrl.GetValue()),
            'score1': self.score1,
            'team2': str(self.team2ctrl.GetValue()),
            'score2': self.score2,
            'team1fg': self.team1cp.get_fg(),
            'team1bg': self.team1cp.get_bg(),
            'team2fg': self.team2cp.get_fg(),
            'team2bg': self.team2cp.get_bg(),
            'fontsize': self.config.get(self.config_section, FontSize.label, ScoreBug.my_default_config[FontSize.label])
            })
        return rv

    def do_fade_on(self, event):
        # CG channel ADD layer template 1 data
        self.parent.transact('CG %d-%d ADD 1 %s 1 %s'%(self.channel(), self.layer(), amcp.quote(self.template()), self.templateData()))

    def do_fade_off(self, event):
        # CG channel STOP layer
        self.parent.transact('CG %d-%d STOP 1'%(self.channel(), self.layer()))

    def team1plus1(self, e):
        self.score1 += 1
        self.do_update()
    def team2plus1(self, e):
        self.score2 += 1
        self.do_update()
    def team1minus1(self, e):
        self.score1 -= 1
        self.do_update()
    def team2minus1(self, e):
        self.score2 -= 1
        self.do_update()

    def do_update_btn(self,e):
        self.config.put(self.config_section, ITEM_TEAM1, self.team1ctrl.GetValue())
        self.config.put(self.config_section, ITEM_TEAM2, self.team2ctrl.GetValue())
        self.config.write()

        self.score1=int(self.score1ctrl.GetValue())
        self.score2=int(self.score2ctrl.GetValue())
        self.do_update()

    def do_update(self):
        # CG channel UPDATE layer data
        self.update_display()
        self.Refresh()
        self.parent.transact('CG %d-%d UPDATE 1 %s'%(self.channel(), self.layer(), self.templateData()))

    def update_field_colours(self):
        if self.team1cp:
            self.team1ctrl.SetBackgroundColour(self.team1cp.get_bg())
            self.team1ctrl.SetForegroundColour(self.team1cp.get_fg())
        if self.team2cp:
            self.team2ctrl.SetBackgroundColour(self.team2cp.get_bg())
            self.team2ctrl.SetForegroundColour(self.team2cp.get_fg())

    def got_colours(self):
        if self.team1cp:
            self.config.put(self.config_section, ITEM_FG1, self.team1cp.get_fg())
            self.config.put(self.config_section, ITEM_BG1, self.team1cp.get_bg())
        if self.team2cp:
            self.config.put(self.config_section, ITEM_FG2, self.team2cp.get_fg())
            self.config.put(self.config_section, ITEM_BG2, self.team2cp.get_bg())
            self.config.write()
        self.update_field_colours()
