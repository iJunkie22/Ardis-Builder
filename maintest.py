#!/usr/bin/python2 -t
from gi.repository import Gtk
import os
import sys

w_path = os.getcwd()
sys.path.append(str(w_path))
import Theme_Indexer

envars = os.environ
user_home_dir = envars['HOME']
Ardis_colors = {}
Ardis_colors = {'Blackish':'#111111', 'Blue':'#0078ad', 'Dark Green':'#66ae4a', 'Light Green':'#79c843', 'Olive Green':'#669966', 'Orange':'#f38725', 'Peach':'#ef6a47', 'Pink':'#e65177', 'Red':'#cd1d31', 'Shadow Grey':'#666666', 'Sky Blue':'#6788cc', 'Soft Red':'#b93d48', 'Violet':'#924565', 'Yellow':'#ffcc67'}

def ardis_dirs(**ArdisDirArgs):
    return '16x16/apps/standard,16x16/devices,16x16/categories,16x16/actions/standard,16x16/mimetypes,16x16/places/'+ArdisDirArgs['places']+',16x16/status,22x22/apps/standard,22x22/devices,22x22/categories,22x22/actions/standard,22x22/mimetypes,22x22/places/'+ArdisDirArgs['places']+',22x22/status,22x22/panel,24x24/apps/standard,24x24/devices,24x24/categories,24x24/actions/standard,24x24/mimetypes,24x24/places/'+ArdisDirArgs['places']+',24x24/panel,24x24/status,32x32/apps,32x32/devices,32x32/categories,32x32/actions/standard,32x32/mimetypes,32x32/places/'+ArdisDirArgs['places']+',32x32/status,48x48/apps,48x48/devices,48x48/categories,48x48/actions/standard,48x48/mimetypes,48x48/places/'+ArdisDirArgs['places']+',48x48/status,64x64/apps,64x64/devices,64x64/categories,64x64/actions/standard,64x64/mimetypes,64x64/places/'+ArdisDirArgs['places']+',64x64/status,96x96/apps,96x96/devices,96x96/categories,96x96/actions/standard,96x96/mimetypes,96x96/places/'+ArdisDirArgs['places']+',96x96/status,128x128/apps,128x128/devices,128x128/categories,128x128/mimetypes,128x128/places/'+ArdisDirArgs['places']+',128x128/status,scalable/apps,scalable/devices,scalable/categories,scalable/actions/standard,scalable/mimetypes,scalable/places/'+ArdisDirArgs['places']+',scalable/status'

def Hide_Page(p_num_to_hide):
    winbox = builder.get_object("box2")
    vp_to_hide = p_num_to_hide+1
    vp_str_to_hide = str(vp_to_hide)
    old_vp = builder.get_object('viewport'+vp_str_to_hide)
    if nextbutton.get_label() == '  Next   ':
        winbox.remove(old_vp)
    
def Show_page(p_num_to_show):
    winbox = builder.get_object("box2")
    vp_to_show = p_num_to_show+1
    vp_str_to_show = str(vp_to_show)
    new_vp = builder.get_object('viewport'+vp_str_to_show)
    
    
    radio_choice_page1 = getPosInCont('event_box_curr_radio1', 'box7')
    label_choice_page1 = getNthChildLabel('box5', radio_choice_page1)
    
    radio_choice_page2 = getPosInCont('event_box_curr_radio2', 'box11')
    label_choice_page2 = getNthChildLabel('box12', radio_choice_page2)
    
    radio_choice_page4 = getPosInCont('event_box_curr_radio4', 'box16')
    label_choice_page4 = getNthChildLabel('box17', radio_choice_page4)
    
    radio_choice_page5 = getPosInCont('event_box_curr_radio5', 'box21')
    label_choice_page5 = getNthChildLabel('box22', radio_choice_page5)
    

    
    
    if label_choice_page5 == 'KDE':
        user_icon_dir = str(user_home_dir+'/.kde/share/icons/')
    elif label_choice_page5 is not None:
        user_icon_dir = str(user_home_dir+'/.icons/')
    else:
        user_icon_dir = None
        
    if vp_to_show > 6:
    #This is when the last page is triggered
        res_label_obj = builder.get_object('results_summary')
        res_sum = str('<b>Action style=</b>'+'"'+label_choice_page1+'"'+'''\n<b>Places color=</b>'''+Ardis_colors[label_choice_page2]+'"'+label_choice_page2+'"'+'''\n<b>Start here=</b>'''+label_choice_page4+'''\n<b>DesktopEnvironment=</b>'''+label_choice_page5+'''\n<b>Install Location=</b>'''+user_icon_dir)
        res_label_obj.set_markup(res_sum)
        d_string = ardis_dirs(places=label_choice_page2)
        ardis_d_list = Theme_Indexer.list_from_string(',', d_string)
        dir_len = len(ardis_d_list)
        prog_step = float('1.0') / float(dir_len)
        prog_bar = builder.get_object('progressbar1')
        prog_bar.set_fraction(float('0.00'))
    if vp_to_show == 7:
        nextbutton.set_label('  Build   ')
        winbox.add(new_vp)
        setPosInCont('curr_page_dot', 'box1', p_num_to_show)

            
    elif nextbutton.get_label() == '  Build   ':
        #The user has chosen to generate
        d_string = ardis_dirs(places=label_choice_page2.lower())
        ardis_d_list = Theme_Indexer.list_from_string(',', d_string)
        dir_len = len(ardis_d_list)
        prog_step = float('1.0') / float(dir_len)
        prog_bar = builder.get_object('progressbar1')
        prog_bar.set_fraction(float('0.00'))
        #prog_bar.set_pulse_step(prog_step)
        #print prog_bar.get_pulse_step()
        temp_theme_file = open(user_icon_dir+"Ardis_TEST_theme/temp_index.theme",'w')
        try:
            temp_theme_file.write('Directories='+d_string+'\n\n')
            for g_item in ardis_d_list[::]:
                g_line = Theme_Indexer.define_group(g_item)
                temp_theme_file.write(g_line+'\n')
                old_prog = prog_bar.get_fraction()
                new_prog = old_prog + prog_step
                prog_bar.set_fraction(new_prog)
                #prog_bar.pulse()
                #print prog_bar.get_fraction()
        finally:
            temp_theme_file.close()
        nextbutton.set_label('  Apply   ')
        
    else:
        try:
            winbox.add(new_vp)
            setPosInCont('curr_page_dot', 'box1', p_num_to_show)

        except TypeError:
            #This captures any attempt to advance to a page that doesnt exist
            
            print 'Action style='+'"'+label_choice_page1+'"'
            #print 'Places color='+Ardis_colors[label_choice_page2], '"'+label_choice_page2+'"'
            print 'Places color='+Ardis_colors[label_choice_page2], '"'+label_choice_page2+'"'
            print 'Start here='+label_choice_page4
            print 'DesktopEnvironment='+label_choice_page5
            print 'Install Location='+user_icon_dir
            
            temp_theme_file = open(user_icon_dir+"Ardis_TEST_theme/temp_index.theme",'r')
            final_theme_file = open(user_icon_dir+"Ardis_TEST_theme/index.theme",'w')
            try:
                final_theme_file.write('[Icon Theme]\nName=ArdisTESTtheme\nComment=Simple and flat icon theme with long shadow - v0.5\n\nDisplayDepth=32\n\nInherits=hicolor,GNOME,Oxygen\n\nExample=folder\n\nLinkOverlay=link\nLockOverlay=lockoverlay\nShareOverlay=share\nZipOverlay=zip\n\nDesktopDefault=48\nDesktopSizes=16,22,32,48,64,128,256\nToolbarDefault=22\nToolbarSizes=16,22,32,48\nMainToolbarDefault=22\nMainToolbarSizes=16,22,32,48\nSmallDefault=16\nSmallSizes=16,22,32,48\nPanelDefault=32\nPanelSizes=16,22,32,48,64,128,256\nDialogDefault=32\nDialogSizes=16,22,32\n\n')
                for line in temp_theme_file:
                    final_theme_file.write(line)
            finally:
                temp_theme_file.close()
                final_theme_file.close()
            

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
        #Captures exit request made by a window manager
        #Disabling this means closing the window leaves a ZOMBIE!!!
        gtkicons = Gtk.IconTheme()
        gtksettings = Gtk.Settings()
        context_list = gtkicons.list_contexts()
        curicontheme = gtkicons.get_default()
        print context_list
        print '.'*50
        print gtkicons.get_search_path()
        print '.'*50
        print curicontheme.get_search_path()
        print '.'*50
        print gtksettings.props.gtk_icon_theme_name
        print '.'*50
        print gtksettings.props.gtk_icon_sizes
        d_string = Theme_Indexer.sample_string('')
        d_list = Theme_Indexer.list_from_string(',', d_string)
        d_test = d_list[4]
        print Theme_Indexer.define_group(d_test)
        Gtk.main_quit()
        exit()

    def on_Next_clicked(self, button):
        #exitbutton.show()
        cur_page = getPosInCont('curr_page_dot', 'box1')
        nex_page = cur_page+1
        Hide_Page(cur_page)
        Show_page(nex_page)
        #if the next page doesnt exist, the app exits now
        setPosInCont('curr_page_dot', 'box1', nex_page)
        #setPageDot(nex_page)
      
    def on_Back_clicked(self, button):
        exitbutton.hide()
        nextbutton.set_label('  Next   ')
        cur_page = getPosInCont('curr_page_dot', 'box1')
        prev_page = cur_page-1
        Hide_Page(cur_page)
        Show_page(prev_page)
        setPosInCont('curr_page_dot', 'box1', prev_page)


    def on_Exit_clicked(self, button):
        exit()
        
    def on_eventbox_radio_press(self, radio, button2):
        cur_page = getPosInCont('curr_page_dot', 'box1')
        active_radio_box = builder.get_object('event_box_curr_radio'+str(cur_page))
        rad_parent = radio.get_parent()
        rad_list = rad_parent.get_children()
        i = rad_list.index(radio)
        rad_parent.reorder_child(active_radio_box, i)
        
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
    return objects_list.index(target_object)
    
def getNthChildLabel(targ_con, child_n):
    taget_container = builder.get_object(targ_con)
    objects_list = taget_container.get_children()
    target_label = objects_list[child_n]
    return target_label.get_text()

def hide_bonus_places(targ_x):
    targ_parent = builder.get_object(targ_x)
    out_list = []
    col_list = targ_parent.get_children()
    r_list = col_list[0].get_children()
    l_list = col_list[1].get_children()
    p_list = col_list[2].get_children()
    for i, v in enumerate(l_list):
        #print i, v.get_text()
        if v.get_text() != "Blue":
            if v.get_text() != "Violet":
                if v.get_text() != "Brown":
                    print v.get_text()
                    out_list.append(r_list[i])
                    out_list.append(p_list[i])
                    out_list.append(l_list[i])
    for i in out_list:
        i.hide()

            

        #if v == radio:
        #    rad_parent.reorder_child(active_radio_box, i)

def hideAdjacentChildren(targ_parent):
    col_list = targ_parent.get_children()
    r_list = col_list[0]
    l_list = col_list[1]
    p_list = col_list[2]


builder = Gtk.Builder()
builder.add_from_file(w_path+'/Ardis setup unified2.glade')
builder.connect_signals(Handler())

window = builder.get_object("window1")
pageDot = builder.get_object("curr_page_dot")
mainbox = builder.get_object("box1")
nextbutton = builder.get_object("button1")
backbutton = builder.get_object("button2")
exitbutton = builder.get_object("button3")
pageone = builder.get_object("viewport1")
hide_bonus_places('box10')
current_page = 0
window.show_all()
backbutton.hide()
exitbutton.hide()
#pageone.show()



Gtk.main()
exit()
