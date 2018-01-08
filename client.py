#!/usr/bin/env python

from Tkinter import * # python-tk package

def stopProg(e):
    root.destroy()

def newlabel(parent, text, col=None, row=None, **kwargs):
    l = Label(parent, text=text, **kwargs)
    l.grid(row=row, column=col)
    return l

class StatusWidget(LabelFrame, object):
    def __init__(self, parent, text='Status', *args, **kwargs):
        super(StatusWidget, self).__init__(*args, text=text, **kwargs)
        self.parent = parent
        self.fStatus = Label(self, width=100, justify=LEFT)
        # TODO text alignment
        self.update('nothing happening')
        self.fStatus.grid(column=1,row=0)
        self.AllOff = parent.newbutton(self, self.allGfxOff, col=2, row=0, text='ALL GFX OFF', bg='#f88', activebackground='#f44')
        # TODO want a safety margin around alloff button

    def update(self, msg):
        #self.status.set(msg)
        self.fStatus.configure(text=msg)

    def allGfxOff(self, e):
        self.parent.wStatus.update('Not yet implemented')

class LowerThird(LabelFrame,object):
    def __init__(self, parent, text='Lower Third', *args, **kwargs):
        super(LowerThird, self).__init__(*args, text=text, **kwargs)
        self.parent = parent

        newlabel(self, 'Line 1: ', 0, 0)
        newlabel(self, 'Line 2: ', 0, 1)
        eTopLine=Entry(self, width=50)
        eTopLine.grid(column=1, row=0)
        eBottomLine=Entry(self, width=50)
        eBottomLine.grid(column=1, row=1)

        bUpdate=self.parent.newbutton(self, self.do_update, text='Update', col=1, row=2)
        # TODO colour choosers / pickers

        newlabel(self, '', 2, 0, width=10) # empty, put some space between the buttons
        bFadeOn=self.parent.newbutton(self, self.fadeOn, col=3, row=0, text='Fade on')
        bFadeOff=self.parent.newbutton(self, self.fadeOff, col=3, row=1, text='Fade off')
        self.pack()

    def fadeOn(self,e):
        # XXX HERE
        self.parent.wStatus.update('Would fade on - Not yet implemented')
    def fadeOff(self,e):
        # XXX HERE
        self.parent.wStatus.update('Would fade off - Not yet implemented')

    def do_update(self,e):
        self.parent.wStatus.update('Would Update - Not yet implemented')


class MainWindow:
    def __init__(self):
        root=Tk()
        self.root = root
        root.title('Hello, Caspar World!')

        self.wStatus = StatusWidget(self)
        self.wStatus.pack()

        self.lt = LowerThird(self)
        self.lt.pack()

    def newbutton(self, parent, targetfunc, col=None, row=None, **kwargs):
        b = Button(parent, **kwargs)
        b.grid(row=row, column=col)
        b.bind('<Button-1>', lambda e: targetfunc(e))
        return b

    def mainloop(self):
        self.root.mainloop()

if __name__=='__main__':
    MainWindow().mainloop()
