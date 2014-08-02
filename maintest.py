#!/usr/bin/python
from gi.repository import Gtk
import os

w_path = os.getcwd()


def Hide_Page(p_num_to_hide):
    winbox = builder.get_object("box2")
    vp_to_hide = p_num_to_hide+1
    vp_str_to_hide = str(vp_to_hide)
    old_vp = builder.get_object('viewport'+vp_str_to_hide)
    winbox.remove(old_vp)
    
def Show_page(p_num_to_show):
    winbox = builder.get_object("box2")
    vp_to_show = p_num_to_show+1
    vp_str_to_show = str(vp_to_show)
    new_vp = builder.get_object('viewport'+vp_str_to_show)
    winbox.add(new_vp)
    setPageDot(p_num_to_show)
    if p_num_to_show == 0:
        backbutton.hide()
    else:
        backbutton.show()


class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)
        exit()

    def on_Next_clicked(self, button):
        exitbutton.show()
        cur_page = getPageDot()
        nex_page = cur_page+1
        Hide_Page(cur_page)
        Show_page(nex_page)
        setPageDot(nex_page)
      
    def on_Back_clicked(self, button):
        exitbutton.hide()
        cur_page = getPageDot()
        prev_page = cur_page-1
        Hide_Page(cur_page)
        Show_page(prev_page)
        setPageDot(prev_page)


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
    
def getPageDot():
    pageDot = builder.get_object("curr_page_dot")
    mainbox = builder.get_object("box1")
    page_dot_list = mainbox.get_children()
    for i, v in enumerate(page_dot_list):
        if v == pageDot:
            return int(i)
    
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
