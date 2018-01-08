#!/usr/bin/env python

from Tkinter import * # python-tk package

def stopProg(e):
    root.destroy()

def transfertext(e):
    label1.configure(text="Hello World")

if __name__=='__main__':
    root=Tk()
    button1=Button(root,
                  text="Hello World click to close")
    button1.pack()
    button1.bind('<Button-1>',stopProg)
    button2=Button(root,text="Click Me")
    button2.pack()
    button2.bind('<Button-1>',transfertext)
    label1=Label(root,text="nothing to say")
    label1.pack()

    root.mainloop()
