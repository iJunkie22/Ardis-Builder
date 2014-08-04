#!/usr/bin/python -t
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
    try:
        winbox.add(new_vp)
        setPosInCont('curr_page_dot', 'box1', p_num_to_show)
    except TypeError:
        Gtk.main_quit()
        exit()
        
    #setPageDot(p_num_to_show)
    setPosInCont('curr_page_dot', 'box1', p_num_to_show)
    if p_num_to_show == 0:
        backbutton.hide()
    else:
        backbutton.show()


class Handler:

    def on_window1_delete_event(self, arg1, arg2):
        Gtk.main_quit()
        exit()

    def on_Next_clicked(self, button):
        exitbutton.show()
        cur_page = getPosInCont('curr_page_dot', 'box1')
        if cur_page == 1:
            radio_choice = getPosInCont('event_box_curr_radio', 'box7')
            print radio_choice
        if cur_page == 2:
            radio_choice = getPosInCont('event_box_curr_radio1', 'box11')
            print radio_choice
        nex_page = cur_page+1
        Hide_Page(cur_page)
        Show_page(nex_page)
        setPosInCont('curr_page_dot', 'box1', nex_page)
        #setPageDot(nex_page)
      
    def on_Back_clicked(self, button):
        exitbutton.hide()
        cur_page = getPosInCont('curr_page_dot', 'box1')
        prev_page = cur_page-1
        Hide_Page(cur_page)
        Show_page(prev_page)
        setPosInCont('curr_page_dot', 'box1', prev_page)


    def on_Exit_clicked(self, button):
        exit()
        
    def on_eventbox_radio_press(self, radio, button2):
        #print radio
        #print button2
        #print "hello world"
        #print builder.get_object("image15")
        active_radio_box = builder.get_object("event_box_curr_radio")
        rad_box1 = builder.get_object("box7")
        rad_list = rad_box1.get_children()
        for i, v in enumerate(rad_list):
            if v == radio:
                #print i
                rad_box1.reorder_child(active_radio_box, i)
            
        
    def on_eventbox_radio_press2(self, radio, button2):
        #print radio
        #print button2
        #print "hello world"
        #print builder.get_object("image15")
        active_radio_box = builder.get_object("event_box_curr_radio1")
        rad_box1 = builder.get_object("box11")
        rad_list = rad_box1.get_children()
        for i, v in enumerate(rad_list):
            if v == radio:
                #print i
                rad_box1.reorder_child(active_radio_box, i)
    def on_inactive_radio_press_event(self, radio):
        rad_box1 = builder.get_object("box7")
        rad_list = rad_box1.get_children()
        for i, v in enumerate(rad_list):
            if v == radio:
                print i
                #return int(i)
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
    
    
def setPosInCont(targ_obj, targ_con, targ_pos):
    target_object = builder.get_object(targ_obj)
    taget_container = builder.get_object(targ_con)
    taget_container.reorder_child(target_object, targ_pos)
    
    
def getPosInCont(targ_obj, targ_con):
    target_object = builder.get_object(targ_obj)
    taget_container = builder.get_object(targ_con)
    objects_list = taget_container.get_children()
    for i, v in enumerate(objects_list):
        if v == target_object:
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
