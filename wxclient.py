#!/usr/bin/env python2
#
# This file is part of Mediary's Caspar Client.
# Copyright (C) 2018 Mediary Limited. All rights reserved.
#

'''
Main entrypoint to the client.

To make this work:
    * You MUST be using Caspar 2.1.0beta or later, 2.0 isn't good enough
    * Install the templates to the caspar server's template directory
'''


import amcp
import traceback
import config
import globalwidget
import lowerthird
import rugby
import scorebug
import wx # developed against wxpython 3.0
import widget

class MainWindow(wx.Frame):
    def __init__(self, parent, title='Mediary\'s Caspar Client', configfile='config.ini'):
        wx.Frame.__init__(self, parent, title=title)
        self.statusbar = self.CreateStatusBar(1, style= wx.STB_SIZEGRIP|wx.STB_SHOW_TIPS|wx.STB_ELLIPSIZE_END|wx.FULL_REPAINT_ON_RESIZE)
        self.status('nothing happening')

        self.config = config.config(configfile)
        self.server = amcp.Connection(self.config, self)

        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(wx.Bitmap('mediary-caspar.ico'))
        self.SetIcon(icon)

        self.panel = MainPanel(self)
        self.Show()

    def status(self, msg):
        ''' If you are going to not return to the main loop for a while,
            you ought to call update() to force a redraw. '''
        self.statusbar.SetStatusText(msg)

    def update(self):
        ''' Redraw. Rarely needed. '''
        self.Update()

class MainPanel(wx.Panel):
    # Master list of widgets
    widgets = [lowerthird.LowerThird, scorebug.ScoreBug, rugby.RugbyScoreBug]

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.gw=None
        self.build()

    config = property(lambda self:self.parent.config)

    def build(self):
        sizer = wx.BoxSizer(wx.VERTICAL)

        if not self.gw:
            self.gw = globalwidget.GlobalWidget(self)
        sizer.Add(self.gw, 1, wx.EXPAND|wx.ALL)

        self.widget_instances = {}
        for w in MainPanel.widgets:
            assert issubclass(w, widget.Widget)
            visible = w.is_visible(self.parent.config)

            instance = None
            if w.ui_label in self.widget_instances:
                instance = self.widget_instances[w.ui_label]

            if not visible:
                if instance:
                    instance.Hide()
                    instance.Destroy()
                    del self.widget_instances[w.ui_label]
                continue

            sizer.AddSpacer(10)
            sizer.AddStretchSpacer()
            if not instance:
                instance = w(self, self.parent.config)
            self.widget_instances[w.ui_label] = instance
            sizer.Add(instance, 0, wx.EXPAND)

        sizer.AddSpacer(10)
        self.SetSizerAndFit(sizer)
        sizer.Fit(self.parent)

    def channel(self):
        ''' For convenient access to our Caspar channel id, which is a configured global '''
        return self.parent.config.channel()

    def status(self, msg):
        ''' If you are going to not return to the main loop for a while,
            you ought to call update() to force a redraw. '''
        self.parent.status(msg)

    def update(self):
        ''' Redraw. Rarely needed. '''
        self.parent.update()

    def transact(self, command):
        '''
            Exception-safe server transaction
            Updates the status line suitably
        '''
        try:
            rv = self.parent.server.transact(command)
            self.status('OK: %s' % command)
            return rv
        except amcp.AMCPException as e:
            self.status('ERROR: %s from %s' % (e, command))
            return None
        except Exception as e:
            print(e)
            traceback.print_exc()
            self.status('ERROR: %s' % e)

if __name__=='__main__':
    app = wx.App(False)
    frame = MainWindow(None)
    app.MainLoop()
