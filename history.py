#!/usr/bin/env python3

#
# This file is part of Mediary's Caspar Client.
# Copyright (C) 2018 Mediary Limited. All rights reserved.
#

'''
Score Bug With History widget
'''

import amcp
import colour
import wx
import sys
from configurable import Configurable,FieldValidator,IntConfigItem,ConfigItem
import configurable
from widget import Widget

ITEM_TEAM1='team1'
ITEM_TEAM2='team2'
ITEM_FG1='team1fg'
ITEM_BG1='team1bg'
ITEM_FG2='team2fg'
ITEM_BG2='team2bg'

class TeamHistoryLine(object):
    def __init__(self, parent, sizer, name='XYZ', initfg='#ffffff', initbg='#0000ff', nboxes=5):
        self.parent = parent
        self.nboxes = nboxes
        self.bigfont = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.smallfont = wx.Font(8, wx.DEFAULT, wx.NORMAL, wx.NORMAL)
        line = wx.BoxSizer(wx.HORIZONTAL)
        # Name field - large
        self.name = wx.TextCtrl(parent, value=name)
        self.name.SetFont(self.bigfont)
        line.Add(self.name, 3, wx.EXPAND)

        # Colour buttons
        self.picker = None #initialisation access loop
        self.picker = colour.PairedColourPicker(parent, notifyfn=self.got_colours, buttonAlabel='FG', buttonBlabel='BG', font=self.smallfont, sizerFlags = wx.VERTICAL, sizerSpace=0, label_patch=None, label_inverse=None, initfg=initfg, initbg=initbg, buttonStyle=wx.BU_EXACTFIT)
        line.Add(self.picker)
        line.AddSpacer(10)

        # Score field
        self.score = wx.TextCtrl(parent, value='0', style=wx.TE_RIGHT)
        line.Add(self.score, 1)
        self.score.SetFont(self.bigfont)
        # colour/size?
        line.AddSpacer(10)

        # History fields (xN) (different colour)
        self.history = []
        for i in range(self.nboxes):
            self.history.append(wx.TextCtrl(parent, value='', style=wx.TE_RIGHT))
            line.Add(self.history[i], 1)

        sizer.Add(line, 0, wx.EXPAND)
        self.update_field_colours()

    def got_colours(self):
        self.parent.colours_changed()
        self.update_field_colours()

    def update_field_colours(self):
        if self.name and self.picker:
            self.name.SetBackgroundColour(self.picker.get_bg())
            self.name.SetForegroundColour(self.picker.get_fg())
            self.parent.Refresh()

    def data(self,prefix):
        ''' Returns a hash of coded data for the template '''
        p=prefix # D.R.Y.
        rv = {}
        # t1n/t2n NAME
        rv['%sn'%p] = self.name.GetValue()
        # t1sc/t2sc MAIN SCORE
        rv['%ssc'%p] = self.score.GetValue()
        for i in range(self.nboxes):
            # t1ssN/t2ssN SUB SCORE / SETS SCORE
            rv['%sss%d'%(p,i+1)] = self.history[i].GetValue()
        # t1bg t2bg t1fg t2fg COLOURS
        rv['%sbg'%p] = self.picker.get_bg()
        rv['%sfg'%p] = self.picker.get_fg()
        return rv

class ScoreHistory(wx.StaticBox, Widget):
    my_configurations=[configurable.Template,configurable.Layer]
    config_section='scorehistory'
    ui_label='Score history'
    my_default_config={'Template': 'mediary/scorehistory',
            'Layer': 102,
            }

    def __init__(self, parent, config, nboxes=5):
        '''
            Required: parent object, config object
        '''
        super(ScoreHistory, self).__init__(parent, label=self.ui_label)
        self.parent = parent
        self.config = config

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        if sys.platform=='win32':
            txt = wx.StaticText(self, wx.ID_ANY, '') # seems to be needed on Windows, otherwise stuff smashes the staticbox label
            sizer.Add(txt)

        # First line: Team 1
        fg = self.config.get(self.config_section, ITEM_FG1, '#ffffff')
        bg = self.config.get(self.config_section, ITEM_BG1, '#ff0000')
        team = self.config.get(self.config_section, ITEM_TEAM1, 'Team 1')
        self.team1 = TeamHistoryLine(self, sizer, team, initbg=bg, initfg=fg, nboxes=nboxes)

        # Second line: Team 2
        fg = self.config.get(self.config_section, ITEM_FG2, '#ffffff')
        bg = self.config.get(self.config_section, ITEM_BG2, '#0000ff')
        team = self.config.get(self.config_section, ITEM_TEAM2, 'Team 2')
        self.team2 = TeamHistoryLine(self, sizer, team, initbg=bg, initfg=fg, nboxes=nboxes)

        # Third line: Free Text
        line3 = wx.BoxSizer(wx.HORIZONTAL)
        line3.AddStretchSpacer(1)
        line3.Add(wx.StaticText(self, wx.ID_ANY, 'Extra'))
        self.extractrl = wx.TextCtrl(self)
        line3.Add(self.extractrl, 1, wx.EXPAND)
        line3.AddStretchSpacer(1)
        sizer.Add(line3, 0, wx.EXPAND)

        # Fourth line: Buttons
        # Take AnimOff CutOff Update

        # Third line: Colour 1, Fade On, Fade Off, Update, Colour 2
        line4 = wx.BoxSizer(wx.HORIZONTAL)

        self.addButton(line4,'TAKE', self.do_anim_on)
        line4.AddStretchSpacer(1)
        self.addButton(line4,'ANIM OFF', self.do_anim_off)
        line4.AddStretchSpacer(1)
        self.addButton(line4, 'CUT OFF', self.do_remove)
        line4.AddStretchSpacer(1)

        self.addButton(line4,'Update', self.do_update)

        line4.AddStretchSpacer(2)

        sizer.AddStretchSpacer()
        sizer.AddSpacer(10)
        sizer.Add(line4, 0, wx.EXPAND)

        if sys.platform.startswith('linux'):
            sizer.AddSpacer(20) # sigh

    def templateData(self):
        rv = {'ex': self.extractrl.GetValue()}
        rv.update(self.team1.data('t1'))
        rv.update(self.team2.data('t2'))
        return amcp.jsondata(rv)

    def do_update(self,e):
        self.config.put(self.config_section, ITEM_TEAM1, self.team1.name.GetValue())
        self.config.put(self.config_section, ITEM_TEAM2, self.team2.name.GetValue())
        self.config.write()
        super(ScoreHistory,self).do_update(e)

    def colours_changed(self):
        self.config.put(self.config_section, ITEM_FG1, self.team1.picker.get_fg())
        self.config.put(self.config_section, ITEM_BG1, self.team1.picker.get_bg())
        self.config.put(self.config_section, ITEM_FG2, self.team2.picker.get_fg())
        self.config.put(self.config_section, ITEM_BG2, self.team2.picker.get_bg())
        self.config.write()

class ScoreHistory1(ScoreHistory):
    '''
        ScoreHistory using only 1 box (e.g. for bowls)
    '''
    def __init__(self, parent, config):
        '''
            Required: parent object, config object
        '''
        super(ScoreHistory1, self).__init__(parent, config, nboxes=1)

if __name__=='__main__':
    import wxclient
    wxclient.run_app([ScoreHistory])
