#
# This file is part of Mediary's Caspar Client.
# Copyright (C) 2018 Mediary Limited. All rights reserved.
#

'''
Global widget for the client.
Contains ALL OFF and global configuration functions.
'''

import wx
import datetime
import sys
from configurable import ConfigItem, IntConfigItem, classproperty
from widget import Widget
from wx.lib.wordwrap import wordwrap

VERSION='0.2+'

Server=ConfigItem('Server', 'IP address or host name of the CasparCG server to connect to')
Port=IntConfigItem('Port', 'Port to connect to (usually 5250)')
Channel=IntConfigItem('Channel', 'CasparCG channel to use')

class GlobalWidget(wx.StaticBox, Widget):
    ui_label='Global'
    my_configurations=[Server,Port,Channel]
    config_section='server'
    my_default_config={'Server':'127.0.0.1', 'Port':5250, 'Channel':1}

    def templateData(self):
        ''' dummy implementation of abstract method, it's ok, we don't use any functions that require it '''
        pass

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

        bAbout = wx.Button(self, label='About')
        bAbout.Bind(wx.EVT_BUTTON, self.do_about)

        bPing = wx.Button(self, label='Ping server')
        bPing.Bind(wx.EVT_BUTTON, self.do_ping)

        bAllOff = wx.Button(self, label='ALL GFX OFF')
        bAllOff.Bind(wx.EVT_BUTTON, self.do_all_off)
        bAllOff.SetBackgroundColour(wx.Colour(255,64,64))
        inner = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(inner, flag=wx.EXPAND)
        inner.Add(bConfig)
        inner.AddSpacer(5)
        inner.Add(bAbout)
        inner.AddSpacer(5)
        inner.Add(bPing)
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
            else:
                self.parent.status('Configuration cancelled')
            dlg.Destroy()

    def do_about(self, event):
        info = wx.AboutDialogInfo()
        info.Name = "Mediary's Caspar Client"
        try:
            icon = wx.Icon('mediary-logo.xpm')
            info.SetIcon(icon)
        except:
            pass
        info.Version = VERSION
        info.Copyright = wordwrap(
                "(C) 2018 Mediary Limited. All rights reserved. "
                "Licensing/business enquiries to: hi@mediary.nz"
                , 350, wx.ClientDC(self.parent))
        #info.Description = wordwrap("...", 350, wx.ClientDC(self.parent))
        info.WebSite = ("https://mediary.nz/", "website")
        #info.Developers = ["Ross Younger"]
        #info.License = wordwrap("...", 500, wx.ClientDC(self.parent))
        wx.AboutBox(info)

    def do_ping(self,event):
        dat = self.parent.transact('VERSION')
        print dat
        if dat:
            self.parent.status('PING: As of %s, server reported version %s'%(datetime.datetime.now(),dat))

def get_server(config):
    return config.get(GlobalWidget.config_section, Server.label, GlobalWidget.my_default_config[Server.label])

def get_port(config):
    return int(config.get(GlobalWidget.config_section, Port.label, GlobalWidget.my_default_config[Port.label]))


def hashkey(cls,config):
    ''' Labels may not be globally unique, so this is what we put in our master ctrls hash '''
    return '%s!%s'%(cls.__name__, config.label)

class ConfigDialog(wx.Dialog):
    def __init__(self, main):
        wx.Dialog.__init__(self, parent=main, title='Configuration', style=wx.DEFAULT_DIALOG_STYLE|wx.RESIZE_BORDER)
        self.main = main
        self.ctrls = {}

        sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(sizer)

        self.configure_widget(GlobalWidget, sizer)

        for cls in self.main.widgets:
            self.configure_widget(cls, sizer)

        sizer.Add(wx.StaticText(self, label='NOTE: Changes to item visibility take effect after quit/reopen'))

        sizer.Add(self.CreateStdDialogButtonSizer(wx.OK|wx.CANCEL))
        size1 = self.GetSize() # plausible horizontal, insufficient vertical
        sizer.Fit(self) # argh: how to make the window wide enough for the horizontal fields?
        size2 = self.GetSize() # short horizontal, good vertical
        self.SetSize((max(size1[0],size2[0]), 30+max(size1[1],size2[1]))) # what a horrid bodge. there must be a better way.
        self.Show()

    def configure_widget(self, cls, parentsizer):
        #print 'WIDGET:', cls, cls.ui_label

        sb = wx.StaticBox(self, label=cls.ui_label)
        sbs = wx.StaticBoxSizer(sb, wx.HORIZONTAL)
        border = wx.BoxSizer()
        border.Add(sbs, 1, border=1)
        parentsizer.Add(border, 0, wx.EXPAND|wx.HORIZONTAL)

        #inner = wx.FlexGridSizer(len(wdg.configurations))
        inner = wx.FlexGridSizer(cols=2, rows=0, vgap=2, hgap=2)
        sbs.Add(inner, 1, 0, border=10)
        inner.AddGrowableCol(1,1)

        defaults = cls.default_config()

        for c in cls.configurations:
            inner.Add(wx.StaticText(sb, label=c.label),0)
            try:
                current = defaults[c.label]
            except KeyError as e:
                print '>> MISSING DEFAULT CONFIG:', cls.__name__+'.'+c.label
                print 'Active defaults is: ', defaults
                raise e
            current = self.main.config.get(cls.config_section, c.label, current)
            ctrl = c.create_control(sb, current)

            self.ctrls[hashkey(cls,c)] = ctrl
            inner.Add(ctrl, flag=wx.EXPAND)

    def read_out(self, config):
        self.read_out_widget(GlobalWidget, config)
        for cls in self.main.widgets:
            self.read_out_widget(cls, config)

    def read_out_widget(self, cls, config):
        for c in cls.configurations:
            val = c.get_value( self.ctrls[hashkey(cls,c)] )
            self.main.config.put(cls.config_section, c.label, val)
