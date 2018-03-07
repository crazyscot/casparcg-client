#!/usr/bin/env python2

import scorebug
import wx
import configurable
import lowerthird
import scoreextra
import timer
import lt_banner

class BasketballScore(scorebug.ScoreBug):
    config_section='basketball'
    ui_label='Basketball'

    def createSecondLine(self,sizer):
        line2 = wx.BoxSizer(wx.HORIZONTAL)
        self.addButton(line2, '+1', lambda e: self.score(1, 1))
        line2.AddSpacer(10)
        self.addButton(line2, '+2', lambda e: self.score(1, 2), True)
        line2.AddSpacer(10)
        self.addButton(line2, '+3', lambda e: self.score(1, 3))

        line2.AddStretchSpacer(1)

        self.addButton(line2, '+1', lambda e: self.score(2, 1))
        line2.AddSpacer(10)
        self.addButton(line2, '+2', lambda e: self.score(2, 2), True)
        line2.AddSpacer(10)
        self.addButton(line2, '+3', lambda e: self.score(2, 3))

        sizer.AddStretchSpacer(1)
        sizer.AddSpacer(10)
        sizer.Add(line2, 0, wx.EXPAND)

if __name__=='__main__':
    import wxclient
    wxclient.run_app([BasketballScore, timer.Timer, scoreextra.ScoreExtra, lowerthird.LowerThird, lt_banner.LowerThirdBanner])
