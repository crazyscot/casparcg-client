
'''
Lower Third widget
'''

import amcp
import colour
import wx
import sys

class LowerThird(wx.StaticBox):
    OPTION_LAYER='layer'
    OPTION_TEMPLATE='template'
    OPTION_BG='bg'
    OPTION_FG='fg'

    def __init__(self, parent, config, label='Lower Third', section='lowerthird'):
        '''
            Required: parent object, config object
            Optional: Frame label, config section to use
        '''
        super(LowerThird, self).__init__(parent, label=label)
        self.parent = parent
        self.config = config
        self.section = section

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
        inner.AddStretchSpacer()
        inner.Add(bFadeOff)
        inner.AddStretchSpacer()
        inner.Add(bUpdate)

        sizer.AddSpacer(10)
        sizer.Add(inner, flag=wx.EXPAND)
        sizer.AddSpacer(10)

        self.cp = None # so the immediate callback works
        self.cp = colour.PairedColourPicker(self,
                self.config.get(self.section, 'fg', '#ffff00'),
                self.config.get(self.section, 'bg', '#0000ff'),
                self.got_colours)
        sizer.Add(self.cp, 1, wx.EXPAND)
        sizer.AddStretchSpacer()

    def channel(self):
        return self.parent.channel()
    def layer(self):
        return self.config.get_int(self.section, LowerThird.OPTION_LAYER, 1)
    def template(self):
        return self.config.get(self.section, LowerThird.OPTION_TEMPLATE, 'lowerthird')
    def fg(self):
        return self.config.get(self.section, LowerThird.OPTION_FG, '#ffff00')
    def bg(self):
        return self.config.get(self.section, LowerThird.OPTION_BG, '#0000ff')

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
            self.config.put(self.section, 'bg', self.cp.get_bg())
            self.config.put(self.section, 'fg', self.cp.get_fg())
            self.config.write()
