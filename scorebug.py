#!/usr/bin/env python2

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

class ScoreBug(wx.StaticBox, Widget):
    my_configurations=[configurable.Template,configurable.Layer]
    config_section='scorebug'
    ui_label='Score bug'
    my_default_config={'Template': 'mediary/scorebug', 'Layer': 102}

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
        self.bigfont = bigfont
        team1 = self.config.get(self.config_section, ITEM_TEAM1, 'AAA')
        self.team1ctrl = wx.TextCtrl(self, 2, value = team1)
        self.team1ctrl.SetFont(bigfont)
        line1.Add(self.team1ctrl, 1)
        self.score1ctrl = wx.TextCtrl(self, 1, value='0', validator=FieldValidator(allowLetters=False))
        self.score1ctrl.SetFont(bigfont)
        line1.Add(self.score1ctrl, 1)

        line1.AddStretchSpacer(1)

        team2 = self.config.get(self.config_section, ITEM_TEAM2, 'BBB')
        self.team2ctrl = wx.TextCtrl(self, value = team2)
        self.team2ctrl.SetFont(bigfont)
        line1.Add(self.team2ctrl, 1)
        self.score2 = 0
        self.score2ctrl = wx.TextCtrl(self, 1, value='0', validator=FieldValidator(allowLetters=False))
        self.score2ctrl.SetFont(bigfont)
        line1.Add(self.score2ctrl, 1)

        sizer.Add(line1, 0, wx.EXPAND)

        # Second line: +1, -1, Update, +1, -1 (overridden in subclasses)
        self.createSecondLine(sizer)

        # Third line: Colour 1, Fade On, Fade Off, Update, Colour 2
        line3 = wx.BoxSizer(wx.HORIZONTAL)

        self.team1cp = self.team2cp = None
        self.team1cp = colour.PairedColourPicker(self,
                self.config.get(self.config_section, ITEM_FG1, '#ffffff'),
                self.config.get(self.config_section, ITEM_BG1, '#0000ff'),
                self.got_colours, label_patch=None, label_inverse=None,
                buttonAlabel='Text colour', buttonBlabel='Background colour')
        line3.Add(self.team1cp, 1, wx.EXPAND)

        line3.AddStretchSpacer(2)

        self.addButton(line3,'TAKE', self.do_anim_on)
        line3.AddStretchSpacer(1)
        self.addButton(line3,'ANIM OFF', self.do_anim_off)
        line3.AddStretchSpacer(1)
        self.addButton(line3, 'CUT OFF', self.do_remove)
        line3.AddStretchSpacer(1)

        self.addButton(line3,'Update', self.do_update)

        line3.AddStretchSpacer(2)

        self.team2cp = colour.PairedColourPicker(self,
                self.config.get(self.config_section, ITEM_FG2, '#ffffff'),
                self.config.get(self.config_section, ITEM_BG2, '#008000'),
                self.got_colours, label_patch=None, label_inverse=None,
                buttonAlabel='Text colour', buttonBlabel='Background colour')
        line3.Add(self.team2cp, 1, wx.EXPAND)

        sizer.AddStretchSpacer()
        sizer.AddSpacer(10)
        sizer.Add(line3, 0, wx.EXPAND)
        self.update_field_colours()

        if sys.platform.startswith('linux'):
            sizer.AddSpacer(20) # sigh

    def createSecondLine(self,sizer):
        line2 = wx.BoxSizer(wx.HORIZONTAL)
        self.addButton(line2,'+1', lambda e: self.score(1, 1), True)
        line2.AddSpacer(10)
        self.addButton(line2,'-1', lambda e: self.score(1, -1))
        line2.AddStretchSpacer(1)
        line2.AddSpacer(10)
        self.addButton(line2,'+1', lambda e: self.score(2, 1), True)
        line2.AddSpacer(10)
        self.addButton(line2,'-1', lambda e: self.score(2, -1))
        sizer.AddStretchSpacer(1)
        sizer.AddSpacer(10)
        sizer.Add(line2, 0, wx.EXPAND)

    def templateData(self):
        rv = amcp.jsondata({
            'team1': str(self.team1ctrl.GetValue()),
            'score1': str(self.score1ctrl.GetValue()),
            'team2': str(self.team2ctrl.GetValue()),
            'score2': str(self.score2ctrl.GetValue()),
            'team1fg': self.team1cp.get_fg(),
            'team1bg': self.team1cp.get_bg(),
            'team2fg': self.team2cp.get_fg(),
            'team2bg': self.team2cp.get_bg(),
            })
        return rv

    def score(self, team, delta):
        if team==1:
            field = self.score1ctrl
        else:
            field = self.score2ctrl
        newscore = int(field.GetValue()) + delta
        field.SetValue(str(newscore))
        self.do_update(None)

    def do_update(self,e):
        self.config.put(self.config_section, ITEM_TEAM1, self.team1ctrl.GetValue())
        self.config.put(self.config_section, ITEM_TEAM2, self.team2ctrl.GetValue())
        self.config.write()
        super(ScoreBug,self).do_update(e)

    def update_field_colours(self):
        if self.team1cp:
            self.team1ctrl.SetBackgroundColour(self.team1cp.get_bg())
            self.team1ctrl.SetForegroundColour(self.team1cp.get_fg())
        if self.team2cp:
            self.team2ctrl.SetBackgroundColour(self.team2cp.get_bg())
            self.team2ctrl.SetForegroundColour(self.team2cp.get_fg())
        self.Refresh()

    def got_colours(self):
        if self.team1cp:
            self.config.put(self.config_section, ITEM_FG1, self.team1cp.get_fg())
            self.config.put(self.config_section, ITEM_BG1, self.team1cp.get_bg())
        if self.team2cp:
            self.config.put(self.config_section, ITEM_FG2, self.team2cp.get_fg())
            self.config.put(self.config_section, ITEM_BG2, self.team2cp.get_bg())
            self.config.write()
        self.update_field_colours()

if __name__=='__main__':
    import wxclient
    wxclient.run_app([ScoreBug])
