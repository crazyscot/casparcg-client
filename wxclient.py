#!/usr/bin/env python2

import amcp
import traceback
import config
import globalwidget
import lowerthird
import wx # developed against wxpython 3.0

'''
Simple Caspar client.
To make this work:
    * You MUST be using Caspar 2.1.0beta or later, 2.0 isn't good enough
    * Install the template to the caspar template directory
    * Write config.ini in the same directory as this script:

        Mandatory config:
            [lowerthird]
            template = TemplateToUse # including directory, e.g. hello-world/lowerthird
            layer = CasparLayerToUse # e.g. 10

            [main]
            channel = CasparChannelToUse # e.g. 1, also used by other widgets

        Optional config:
            [lowerthird]
            fg = #0000ff # Foreground colour - text & ruler - specify as #RRGGBB (hex)
            bg = #ffff00 # Background for the box - #RRGGBB (hex)

            [server]
            host = hostname or IP address # default 127.0.0.1
            port = 1234 # default 5250
'''

class MainWindow(wx.Frame):
    def __init__(self, parent, title='Hello, Caspar World!', configfile='config.ini'):
        wx.Frame.__init__(self, parent, title=title)
        self.statusbar = self.CreateStatusBar(1, style= wx.STB_SIZEGRIP|wx.STB_SHOW_TIPS|wx.STB_ELLIPSIZE_END|wx.FULL_REPAINT_ON_RESIZE)
        self.status('nothing happening')

        self.config = config.config(configfile)
        self.server = amcp.Connection(self.config, self)

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
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        sizer = wx.BoxSizer(wx.VERTICAL)

        gw = globalwidget.GlobalWidget(self)
        sizer.Add(gw, 0, wx.EXPAND)

        sizer.AddSpacer(10)
        sizer.AddStretchSpacer()

        # TODO make the set of visible widgets configurable
        self.lt = lowerthird.LowerThird(self, self.parent.config)
        sizer.Add(self.lt, 0, wx.EXPAND)

        sizer.AddSpacer(10)
        self.SetSizerAndFit(sizer)
        sizer.Fit(parent)

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
