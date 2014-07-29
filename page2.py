#!/usr/bin/python
from gi.repository import Gtk
import os

w_path = os.getcwd()
print w_path

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)
        exit()

    def onNextPressed(self, button):
        #print("Hello World!")
        radio1 = builder.get_object("radiobutton1")
        radio2 = builder.get_object("radiobutton2")
        radio3 = builder.get_object("radiobutton3")
        radio4 = builder.get_object("radiobutton4")
        
        def active_check(radio):
		if radio.get_active() is True:
			print radio.get_property("label")
		else:
			return None
		
	active_check(radio1)
	active_check(radio2)
	active_check(radio3)
	active_check(radio4)
        
        button.get_property("label")
        #setPageDot(2)
        #nextPage()
        #pageone.hide()
        exit()
        
def setPageDot(n):
    pageDot = builder.get_object("curr_page_dot")
    mainbox = builder.get_object("box1")
    mainbox.reorder_child(pageDot, n)
    
def getPosOf(objbox, obj):
    obj_item = builder.get_object(obj)
    obj_box = builder.get_object(objbox)

    obj_box.child_get_property(obj_item, "position", int)
    #return get_int(value())
    
def nextPage():
	c = getPosOf("box1", "curr_page_dot")
	print c
	nexp = c+1
	setPageDot(nexp)

builder = Gtk.Builder()
builder.add_from_file(w_path+'/Ardis setup style.glade')
builder.connect_signals(Handler())

window = builder.get_object("window1")
pageDot = builder.get_object("curr_page_dot")
mainbox = builder.get_object("box1")
pageone = builder.get_object("viewport1")
pagetest = mainbox.query_child_packing(pageDot)
current_page = 1
#print pagetest
setPageDot(current_page)
window.show_all()
pageone.show()



Gtk.main()
exit()
