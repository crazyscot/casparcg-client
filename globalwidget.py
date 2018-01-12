
'''
Global widget for the client.
Contains ALL OFF and global configuration functions.
'''

import wx
import sys

class GlobalWidget(wx.StaticBox):
    def __init__(self, parent):
        '''
            Parent must accept status() calls and have a config member
        '''
        super(GlobalWidget, self).__init__(parent, label='Global')
        self.parent = parent

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        if sys.platform=='win32':
            txt = wx.StaticText(self, wx.ID_ANY, '') # seems to be needed on Windows, otherwise stuff smashes the staticbox label
            sizer.Add(txt)

        bConfig = wx.Button(self, label='Configuration')
        bConfig.Bind(wx.EVT_BUTTON, self.do_config)

        bAllOff = wx.Button(self, label='ALL GFX OFF')
        bAllOff.Bind(wx.EVT_BUTTON, self.do_all_off)
        bAllOff.SetBackgroundColour(wx.Colour(255,64,64))
        inner = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(inner, flag=wx.EXPAND)
        inner.Add(bConfig)
        inner.AddStretchSpacer()
        inner.Add(bAllOff)

        if sys.platform.startswith('linux'):
            sizer.AddSpacer(20) # sigh

    def do_all_off(self, event):
        self.parent.transact('CLEAR %d'%(self.parent.channel()))

    def do_config(self, event):
        '''
            Master configuration dialog
        '''
        with ConfigDialog(self.parent) as dlg:
            result = dlg.ShowModal()
            if result == wx.ID_OK:
                self.parent.status('Reconfigured')
                dlg.read_out(self.parent.config)
                self.parent.config.write()
                # XXX Parent rebuild for visibility
            else:
                self.parent.status('Configuration cancelled')
            dlg.Destroy()

class ConfigDialog(wx.Dialog):
    def __init__(self, main):
        wx.Dialog.__init__(self, parent=None, title='Configuration', style=wx.RESIZE_BORDER)
        self.main = main
        self.ctrls = {}

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        # TODO Global config - server, channel - add this to the GlobalWidget
        for (lbl,wdg) in self.main.widget_instances.items():
            self.configure_widget(wdg, sizer)
            #sizer.AddStretchSpacer()

        sizer.Add(self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL))
        self.Centre()
        #sizer.Fit(self)
        self.Show()

    def configure_widget(self, wdg, parentsizer):
        #print 'WIDGET:', wdg.__class__, wdg.ui_label

        sb = wx.StaticBox(self, label=wdg.ui_label)
        sbs = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        border = wx.BoxSizer()
        border.Add(sbs, 1, wx.EXPAND|wx.HORIZONTAL, border=1)
        parentsizer.Add(border, 1, wx.EXPAND|wx.HORIZONTAL)

        #inner = wx.FlexGridSizer(len(wdg.configurations))
        inner = wx.FlexGridSizer(cols=2, rows=0, vgap=2, hgap=2)
        sbs.Add(inner, 1, wx.ALL|wx.EXPAND, border=10)
        inner.AddGrowableCol(1,1)
        inner.SetFlexibleDirection(wx.HORIZONTAL)
        #inner.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)

        defaults = wdg.default_config()

        for c in wdg.configurations:
            #print '>> CONFIG:', c.label
            inner.Add(wx.StaticText(self, label=c.label),0)
            current = defaults[c.label]
            current = self.main.config.get(wdg.config_section, c.label, current)
            ctrl = wx.TextCtrl(self, value=str(current))
            self.ctrls[c.label] = ctrl
            inner.Add(ctrl, 1, wx.EXPAND|wx.HORIZONTAL)

        #inner.Layout()

    def read_out(self, config):
        # TODO action global config too
        for (lbl,wdg) in self.main.widget_instances.items():
            self.read_out_widget(wdg, config)

    def read_out_widget(self, wdg, config):
        for c in wdg.configurations:
            val = self.ctrls[c.label].GetValue()
            self.main.config.put(wdg.config_section, c.label, val)
