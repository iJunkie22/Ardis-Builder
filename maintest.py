#!/usr/bin/python
from gi.repository import Gtk
import os

w_path = os.getcwd()



class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)
        exit()
        
    def on_Next_clicked(self, button):
	backbutton.show()
	exitbutton.show()
	winbox = builder.get_object("box2")
	page1_viewport = builder.get_object("viewport1")
	page2_viewport = builder.get_object("viewport2")
	setPageDot(1)
	winbox.remove(page1_viewport)
	winbox.add(page2_viewport)
      
    def on_Back_clicked(self, button):
	backbutton.hide()
	exitbutton.hide()
	winbox = builder.get_object("box2")
	page1_viewport = builder.get_object("viewport1")
	page2_viewport = builder.get_object("viewport2")
	setPageDot(0)
	winbox.remove(page2_viewport)
	winbox.add(page1_viewport)
	
    def on_Exit_clicked(self, button):
	exit()
      

    def onButtonPressed(self, button):
	try:
	  execfile(w_path+'/page2.py')
	  setPageDot(1)
	  pageone.hide()
        finally:
	  winbox = builder.get_object("box2")
	  page1_viewport = builder.get_object("viewport1")
	  page2_viewport = builder.get_object("viewport2")
	  #page_viewport.hide()
	  setPageDot(1)
	  winbox.remove(page1_viewport)
	  winbox.add(page2_viewport)
	  #exit()
        
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
backbutton = builder.get_object("button2")
exitbutton = builder.get_object("button3")
pageone = builder.get_object("viewport1")
pagetest = mainbox.query_child_packing(pageDot)
current_page = 0
#print pagetest
window.show_all()
backbutton.hide()
exitbutton.hide()
pageone.show()



Gtk.main()
exit()
