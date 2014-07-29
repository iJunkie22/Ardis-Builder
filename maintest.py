#!/usr/bin/python
from gi.repository import Gtk
import os

w_path = os.getcwd()

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)
        exit()

    def onButtonPressed(self, button):
        print("./page2.py")
        setPageDot(1)
        pageone.hide()
        exit()
        
def setPageDot(n):
    pageDot = builder.get_object("curr_page_dot")
    mainbox = builder.get_object("box1")
    mainbox.reorder_child(pageDot, n)
    
def nextPage(c):
    nexp = c+1
    setPageDot(nexp)
    return nexp

builder = Gtk.Builder()
builder.add_from_file(w_path+'/Ardis setup unified.glade')
builder.connect_signals(Handler())

window = builder.get_object("window1")
pageDot = builder.get_object("curr_page_dot")
mainbox = builder.get_object("box1")
pageone = builder.get_object("viewport1")
pagetest = mainbox.query_child_packing(pageDot)
current_page = 0
#print pagetest
window.show_all()
pageone.show()



Gtk.main()
exit()
