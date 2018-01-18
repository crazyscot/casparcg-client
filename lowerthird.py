
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
    OPTION_BG='bg'
    OPTION_FG='fg'

    my_configurations=[configurable.Template,configurable.Layer]
    config_section='lowerthird'
    ui_label='Lower Third'
    my_default_config={'Template': 'hello-world/helloworld', 'Layer': 10}

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

        bFadeOn = wx.Button(self, label='Fade on')
        bFadeOn.Bind(wx.EVT_BUTTON, self.do_fade_on)
        bFadeOff = wx.Button(self, label='Fade off')
        bFadeOff.Bind(wx.EVT_BUTTON, self.do_fade_off)
        bUpdate = wx.Button(self, label='Update')
        bUpdate.Bind(wx.EVT_BUTTON, self.do_update)

        inner = wx.BoxSizer(wx.HORIZONTAL)
        inner.Add(bFadeOn)
        inner.AddSpacer(10)
        inner.Add(bFadeOff)
        inner.AddSpacer(10)
        inner.Add(bUpdate)

        inner.AddSpacer(20)
        inner.AddStretchSpacer(1)
        self.cp = None # so the immediate callback works
        self.cp = colour.PairedColourPicker(self,
                self.config.get(self.config_section, 'fg', '#ffff00'),
                self.config.get(self.config_section, 'bg', '#0000ff'),
                self.got_colours)
        inner.Add(self.cp, 1, wx.EXPAND)

        sizer.AddSpacer(10)
        sizer.Add(inner, flag=wx.EXPAND)
        sizer.AddSpacer(20)

        sizer.AddStretchSpacer()

    def channel(self):
        return self.parent.channel()
    def layer(self):
        return self.config.get_int(self.config_section, configurable.Layer.label, 1)
    def template(self):
        return self.config.get(self.config_section, configurable.Template.label, 'lowerthird')
    def fg(self):
        return self.config.get(self.config_section, LowerThird.OPTION_FG, '#ffff00')
    def bg(self):
        return self.config.get(self.config_section, LowerThird.OPTION_BG, '#0000ff')

    def templateData(self):
        return amcp.jsondata({
            'f0': self.line1.GetValue(),
            'f1': self.line2.GetValue(),
            'bgcol': self.cp.get_bg(),
            'fgcol': self.cp.get_fg(),
            })

    def do_fade_on(self, event):
        # CG channel ADD layer template 1 data
        self.parent.transact('CG %d ADD %d %s 1 %s'%(self.channel(), self.layer(), amcp.quote(self.template()), self.templateData()))

    def do_fade_off(self, event):
        # CG channel STOP layer
        self.parent.transact('CG %d STOP %d'%(self.channel(), self.layer()))

    def do_update(self,e):
        # CG channel UPDATE layer data
        self.parent.transact('CG %d UPDATE %d %s'%(self.channel(), self.layer(), self.templateData()))

    def got_colours(self):
        if self.cp:
            self.config.put(self.config_section, 'bg', self.cp.get_bg())
            self.config.put(self.config_section, 'fg', self.cp.get_fg())
            self.config.write()
