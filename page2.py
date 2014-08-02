#!/usr/bin/python
from gi.repository import Gtk
import os

w_path = os.getcwd()
print w_path
gtkstyle = Gtk.CssProvider()
cust_style = gtkstyle.new()
cust_stle.load_from_file('ArdisGTKStyle.css')

class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)
        exit()

    def onNextPressed(self, button):
        #print("Hello World!")
        radio1 = builder2.get_object("radiobutton1")
        radio2 = builder2.get_object("radiobutton2")
        radio3 = builder2.get_object("radiobutton3")
        radio4 = builder2.get_object("radiobutton4")
        
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
    pageDot = builder2.get_object("curr_page_dot")
    mainbox = builder2.get_object("box1")
    mainbox.reorder_child(pageDot, n)
    
def getPosOf(objbox, obj):
    obj_item = builder2.get_object(obj)
    obj_box = builder2.get_object(objbox)

    obj_box.child_get_property(obj_item, "position", int)
    #return get_int(value())
    
def nextPage():
	c = getPosOf("box1", "curr_page_dot")
	print c
	nexp = c+1
	setPageDot(nexp)

builder2 = Gtk.Builder()
builder2.add_from_file(w_path+'/Ardis setup style.glade')
builder2.connect_signals(Handler())

window = builder2.get_object("window1")
pageDot = builder2.get_object("curr_page_dot")
mainbox = builder2.get_object("box1")
pageone = builder2.get_object("viewport1")
pagetest = mainbox.query_child_packing(pageDot)
current_page = 1
#print pagetest

setPageDot(current_page)
window.show_all()
pageone.show()



Gtk.main()
exit()
