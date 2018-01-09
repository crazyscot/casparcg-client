'''
    Paired colour picker widgetry
'''

import wx

class ColourPicker(wx.Button):
    '''
        Widget for triggering a colour picker
        Colours are stored internally as wx.Colour, converted by get()
    '''
    def __init__(self, parent, label, initial):
        ''' Initial value should be an HTML #rrggbb triplet (though can be anything that wx.Colour.Set() accepts) '''
        super(ColourPicker, self).__init__(parent, label=label)
        self.current = wx.Colour()
        self.current.SetFromString(initial)
        self.parent = parent
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
    def __init__(self, parent, initfg='#ffff00', initbg='#0000ff', notifyfn=None):
        super(PairedColourPicker, self).__init__(parent)
        self.parent = parent
        self.notifyfn = notifyfn

        sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(sizer)
        self.fg = ColourPicker(self, 'Text colour', initfg )
        self.bg = ColourPicker(self, 'Background', initbg )
        sizer.Add(self.fg, flag=wx.EXPAND)
        sizer.Add(self.bg, flag=wx.EXPAND)

        self.patch = wx.Panel(self)
        self.patchtext = wx.StaticText(self.patch, label=' Sample ')
        font = wx.Font(18, wx.NORMAL, wx.NORMAL, wx.BOLD)
        self.patchtext.SetFont(font)
        inner = wx.BoxSizer(wx.VERTICAL)
        self.patch.SetSizer(inner)
        inner.Add(self.patchtext, 0, wx.CENTRE)

        sizer.AddStretchSpacer()
        sizer.Add(self.patch, flag=wx.EXPAND)
        sizer.AddStretchSpacer()
        self.update_patch()

    def update_patch(self):
        self.patch.SetBackgroundColour(self.bg.current)
        self.patchtext.SetForegroundColour(self.fg.current)
        if self.notifyfn:
            self.notifyfn()

    def get_bg(self):
        return self.bg.get()
    def get_fg(self):
        return self.fg.get()
