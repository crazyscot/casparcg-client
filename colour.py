#
# This file is part of Mediary's Caspar Client.
# Copyright (C) 2018 Mediary Limited. All rights reserved.
#

'''
    Paired colour picker widgetry
'''

import wx

class ColourPicker(wx.Button):
    '''
        Widget for triggering a colour picker
        Colours are stored internally as wx.Colour, converted by get()
    '''
    def __init__(self, parent, label, initial, font=None, style=0):
        ''' Initial value should be an HTML #rrggbb triplet (though can be anything that wx.Colour.Set() accepts) '''
        super(ColourPicker, self).__init__(parent, label=label, style=style)
        self.current = wx.Colour()
        self.current.Set(initial)
        self.parent = parent
        if font:
            self.SetFont(font)
        self.Bind(wx.EVT_BUTTON, self.do_pick)

    def do_pick(self, event):
        data = wx.ColourData()
        #data.SetChooseFull(True)
        data.SetColour(self.current)
        dlg = wx.ColourDialog(self, data)
        if dlg.ShowModal() == wx.ID_OK:
            self.current = dlg.GetColourData().Colour
            self.parent.update_patch()
        dlg.Destroy()

    def get(self):
        ''' Returns the internal wxColour as an RGB triplet '''
        return self.current.GetAsString(wx.C2S_HTML_SYNTAX)

class PairedColourPicker(wx.Panel):
    '''
        Widget for choosing a pair of colours for text.
    '''
    def __init__(self, parent, initfg='#ffff00', initbg='#0000ff', notifyfn=None, label_patch=' A on B ', label_inverse=' B on A ', buttonAlabel='Colour A', buttonBlabel='Colour B', font=None, sizerFlags = wx.HORIZONTAL, sizerSpace = 10, buttonStyle=0):
        super(PairedColourPicker, self).__init__(parent)
        self.parent = parent
        self.notifyfn = notifyfn
        self.patch = self.patch2 = None

        sizer = wx.BoxSizer(sizerFlags)
        self.SetSizer(sizer)
        self.fg = ColourPicker(self, buttonAlabel, initfg, font, buttonStyle)
        self.bg = ColourPicker(self, buttonBlabel, initbg, font, buttonStyle)
        sizer.Add(self.fg)
        sizer.AddSpacer(sizerSpace)
        sizer.Add(self.bg)

        if label_patch is not None:
            self.patch = wx.Panel(self)
            self.patchtext = wx.StaticText(self.patch, label=label_patch)
            font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)
            self.patchtext.SetFont(font)
            inner = wx.BoxSizer(wx.VERTICAL)
            self.patch.SetSizer(inner)
            inner.Add(self.patchtext, 0, wx.CENTRE)

            sizer.AddSpacer(10)
            sizer.Add(self.patch, flag=wx.LEFT|wx.RIGHT, border=5)
            self.update_patch()
        else:
            self.patch = None

        if label_inverse is not None:
            self.patch2 = wx.Panel(self)
            self.patch2text = wx.StaticText(self.patch2, label=label_inverse)
            font = wx.Font(18, wx.DEFAULT, wx.NORMAL, wx.BOLD)
            self.patch2text.SetFont(font)
            inner = wx.BoxSizer(wx.VERTICAL)
            self.patch2.SetSizer(inner)
            inner.Add(self.patch2text, 0, wx.CENTRE)

            sizer.AddSpacer(10)
            sizer.Add(self.patch2, flag=wx.LEFT|wx.RIGHT, border=5)
            self.update_patch()
        else:
            self.patch2 = None

    def update_patch(self):
        if self.patch:
            self.patch.SetBackgroundColour(self.bg.current)
            self.patchtext.SetForegroundColour(self.fg.current)
        if self.patch2:
            self.patch2.SetBackgroundColour(self.fg.current)
            self.patch2text.SetForegroundColour(self.bg.current)
        if self.notifyfn:
            self.notifyfn()

    def get_bg(self):
        return self.bg.get()
    def get_fg(self):
        return self.fg.get()
