
'''
Global widget for the client.
Contains ALL OFF and global configuration functions.
'''

import wx
import sys
from configurable import ConfigItem, classproperty
from widget import Widget

class Server(ConfigItem):
    label='Server'
    helptext='IP address or host name of the CasparCG server to connect to'
class Port(ConfigItem):
    label='Port'
    helptext='Port to connect to (usually 5250)'
class Channel(ConfigItem):
    label='Channel'
    helptext='CasparCG channel to use'

class GlobalWidget(wx.StaticBox, Widget):
    ui_label='Global'
    my_configurations=[Server,Port,Channel]
    config_section='server'
    my_default_config={'Server':'127.0.0.1', 'Port':5250, 'Channel':1}

    @classproperty
    def configurations(cls):
        ''' This widget does not have a Visible member '''
        return cls.my_configurations[:]

    def __init__(self, parent):
        '''
            Parent must accept status() calls and have a config member
        '''
        super(GlobalWidget, self).__init__(parent, label=self.ui_label)
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
                self.parent.rebuild()
            else:
                self.parent.status('Configuration cancelled')
            dlg.Destroy()

class ConfigDialog(wx.Dialog):
    def __init__(self, main):
        wx.Dialog.__init__(self, parent=main, title='Configuration', style=wx.RESIZE_BORDER)
        self.main = main
        self.ctrls = {}

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        # TODO Global config - server, channel - add this to the GlobalWidget
        for cls in self.main.widgets:
            self.configure_widget(cls, sizer)
            #sizer.AddStretchSpacer()

        sizer.Add(self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL))
        self.Centre()
        #sizer.Fit(self)
        self.Show()

    def configure_widget(self, cls, parentsizer):
        #print 'WIDGET:', cls, cls.ui_label

        sb = wx.StaticBox(self, label=cls.ui_label)
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

        defaults = cls.default_config()

        for c in cls.configurations:
            #print '>> CONFIG:', c.label
            inner.Add(wx.StaticText(self, label=c.label),0)
            current = defaults[c.label]
            current = self.main.config.get(cls.config_section, c.label, current)
            ctrl = wx.TextCtrl(self, value=str(current))
            self.ctrls[c.label] = ctrl
            ctrl.SetToolTip(wx.ToolTip(c.helptext))
            inner.Add(ctrl, 1, wx.EXPAND|wx.HORIZONTAL)

        #inner.Layout()

    def read_out(self, config):
        # TODO action global config too
        for cls in self.main.widgets:
            self.read_out_widget(cls, config)

    def read_out_widget(self, cls, config):
        for c in cls.configurations:
            val = self.ctrls[c.label].GetValue()
            self.main.config.put(cls.config_section, c.label, val)
