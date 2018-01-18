
'''
Lower Third widget
'''

import amcp
import colour
import wx
import sys
from configurable import Configurable,FieldValidator
import configurable
from widget import Widget

ITEM_TEAM1='team1'
ITEM_TEAM2='team2'

class ScoreBug(wx.StaticBox, Widget):
    my_configurations=[configurable.Template,configurable.Layer]
    config_section='scorebug'
    ui_label='Score bug'
    my_default_config={'Template': 'hello-world/scorebug', 'Layer': 20}

    def __init__(self, parent, config):
        '''
            Required: parent object, config object
        '''
        super(ScoreBug, self).__init__(parent, label=self.ui_label)
        self.parent = parent
        self.config = config

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        # TODO win32 bodge here if necessary

        # First line: Team names and scores

        line1 = wx.BoxSizer(wx.HORIZONTAL)
        bigfont = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        self.team1 = self.config.get(self.config_section, 'team1', 'AAA')
        self.team1ctrl = wx.TextCtrl(self, 2, value = self.team1)
        self.team1ctrl.SetFont(bigfont)
        line1.Add(self.team1ctrl, 1)
        self.score1 = 0
        self.score1ctrl = wx.TextCtrl(self, 1, value='', validator=FieldValidator(allowLetters=False))
        self.score1ctrl.SetFont(bigfont)
        line1.Add(self.score1ctrl, 1)

        line1.AddStretchSpacer(1)

        self.team2 = self.config.get(self.config_section, 'team2', 'BBB')
        self.team2ctrl = wx.TextCtrl(self, value = self.team2)
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

        # Third line: Fade On, Fade Off, Update
        line3 = wx.BoxSizer(wx.HORIZONTAL)
        lineX = line3
        addButton('Fade on', self.do_fade_on)
        line3.AddStretchSpacer(1)
        addButton('Fade off', self.do_fade_off)
        line3.AddStretchSpacer(1)
        addButton('Update', self.do_update_btn)
        sizer.AddStretchSpacer(10)
        sizer.AddSpacer(10)
        sizer.Add(line3, 0, wx.EXPAND)

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
            'team1': self.team1,
            'score1': self.score1,
            'team2': self.team2,
            'score2': self.score2,
            })
        # TODO: team1bg, team1fg, team2bg, team2fg
        return rv

    def do_fade_on(self, event):
        # CG channel ADD layer template 1 data
        self.parent.transact('CG %d ADD %d %s 1 %s'%(self.channel(), self.layer(), amcp.quote(self.template()), self.templateData()))

    def do_fade_off(self, event):
        # CG channel STOP layer
        self.parent.transact('CG %d STOP %d'%(self.channel(), self.layer()))

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
        self.team1=self.team1ctrl.GetValue()
        self.team2=self.team2ctrl.GetValue()

        self.config.put(self.config_section, ITEM_TEAM1, self.team1)
        self.config.put(self.config_section, ITEM_TEAM2, self.team2)
        self.config.write()

        self.score1=int(self.score1ctrl.GetValue())
        self.score2=int(self.score2ctrl.GetValue())
        self.do_update()

    def do_update(self):
        # CG channel UPDATE layer data
        self.update_display()
        self.Refresh()
        self.parent.transact('CG %d UPDATE %d %s'%(self.channel(), self.layer(), self.templateData()))
