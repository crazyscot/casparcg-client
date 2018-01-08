#!/usr/bin/env python

from Tkinter import * # python-tk package

def stopProg(e):
    root.destroy()

def nyi():
    wStatus.update('Not yet implemented')

def fadeOn(e):
    # XXX HERE
    wStatus.update('Would fade on - Not yet implemented')
def fadeOff(e):
    # XXX HERE
    wStatus.update('Would fade off - Not yet implemented')
def do_update(e):
    nyi()
def allGfxOff(e):
    nyi()

def newlabel(parent, text, col=None, row=None, **kwargs):
    l = Label(parent, text=text, **kwargs)
    l.grid(row=row, column=col)
    return l

def newbutton(parent, target, col=None, row=None, **kwargs):
    b = Button(parent, **kwargs)
    b.grid(row=row, column=col)
    b.bind('<Button-1>', target)
    return b

class StatusWidget(Frame, object):
    def __init__(self, *args, **kwargs):
        super(StatusWidget, self).__init__(*args, **kwargs)
        newlabel(self, 'Status: ', 0, 0)
        self.fStatus = Label(self, width=100, justify=LEFT)
        self.update('nothing happening')
        self.fStatus.grid(column=1,row=0)
        self.AllOff = newbutton(self, allGfxOff, col=2, row=0, text='ALL GFX OFF', bg='#f88', activebackground='#f44')
        # TODO want a safety margin around alloff button

    def update(self, msg):
        #self.status.set(msg)
        self.fStatus.configure(text=msg)

if __name__=='__main__':
    root=Tk()
    root.title('Hello, Caspar World!')
    # set window title

    wStatus = StatusWidget(root)
    wStatus.pack()

    fr = Frame(root, bd=10)
    newlabel(fr, 'Line 1: ', 0, 0)
    newlabel(fr, 'Line 2: ', 0, 1)
    eTopLine=Entry(fr, width=50)
    eTopLine.grid(column=1, row=0)
    eBottomLine=Entry(fr, width=50)
    eBottomLine.grid(column=1, row=1)

    bUpdate=newbutton(fr, do_update, text='Update', col=1, row=2)
    fr.pack()

    # TODO colour choosers / pickers

    fr = Frame(root, bd=20)
    bFadeOn=newbutton(fr, fadeOn, text='Fade on')
    bFadeOff=newbutton(fr, fadeOff, text='Fade off')
    fr.pack()

    root.mainloop()
