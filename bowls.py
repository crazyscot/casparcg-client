#!/usr/bin/env python2

#
# This file is part of Mediary's Caspar Client.
# Copyright (C) 2018 Mediary Limited. All rights reserved.
#

'''
Lawn bowls ends widget
'''

import amcp
import wx
import sys
from configurable import Configurable,FieldValidator
import configurable
from widget import Widget
import datetime
from scoreextra import ScoreExtra
import scorebug
import lowerthird

class BowlsEnds(ScoreExtra):
    my_configurations=[configurable.Template,configurable.Layer]
    config_section='Bowls Ends'
    ui_label='Bowls Ends'
    my_default_config={'Template': 'mediary/scoreextra', 'Layer': 104}

    def createControl(self, sizer):
        self.n_end = wx.TextCtrl(self, value='1', validator=FieldValidator(allowLetters=False))
        sizer.Add(self.n_end, 1, flag=wx.EXPAND)
        sizer.AddSpacer(10)
        self.addButton(sizer,'Next End', self.do_next_end)
        sizer.AddStretchSpacer(1)
        self.addButton(sizer,'Final Score', self.do_final_score)
        sizer.AddStretchSpacer(1)

    def templateData(self):
        e = self.n_end.GetValue()
        if e == u'F':
            msg='FINAL SCORE'
        else:
            msg = 'END '+str(e)
        rv = amcp.jsondata({
            'line1': msg,
            })
        return rv

    def do_next_end(self, event):
        n = self.n_end.GetValue()
        if n == u'F':
            n = 1
        else:
            n = int(n) + 1
        self.n_end.SetValue(str(n))
        self.do_update(None)

    def do_final_score(self,event):
        self.n_end.SetValue(u'F')
        self.do_update(None)

if __name__=='__main__':
    import wxclient
    wxclient.run_app([scorebug.ScoreBug, BowlsEnds, lowerthird.LowerThird])
