#!/usr/bin/python2 -t
#coding: utf-8
import gi
gi.require_version('Gtk', '3.0')
# Credit for this patch goes to https://build.opensuse.org/package/view_file/openSUSE:12.3/alacarte/alacarte-force-Gtk3.patch?expand=1
from gi.repository import Gtk
import os
import sys
import re
import glob

w_path = os.getcwd()
sys.path.append(str(w_path))
import Theme_Indexer
envars = {}
user_GDMS = None
envars = os.environ.copy()
user_home_dir = envars['HOME']
user_DE = envars.get('XDG_CURRENT_DESKTOP')
if user_DE is None:
    # The GDM doesnt declare the fairly new (added ~2014) XDG_CURRENT_DESKTOP global...
    user_GDMS = envars.get('GDMSESSION')
    if user_GDMS == 'kde-plasma':
        user_DE = 'KDE'
    else:
        user_DE = user_GDMS

def find_theme_path(themedir):
    icon_theme_locs = []
    if user_DE == 'KDE':
        icon_theme_locs.append(os.path.expanduser('~/.kde/share/icons'))
        icon_theme_locs.append(os.path.expanduser('~/.kde4/share/icons'))
        icon_theme_locs.append(os.path.expanduser('~/.icons'))
    else:
        icon_theme_locs.append(os.path.expanduser('~/.icons'))
    icon_theme_locs.append('/usr/share/icons')
    for themes_d in icon_theme_locs:
        pos_theme_path = os.path.join(themes_d, themedir)
        if os.path.isdir(pos_theme_path):
            return pos_theme_path
            break

def parse_file(indexfile, targ_group):
    new_dict = {}
    nf = open(indexfile, 'r')
    try:
        new_dict = {}
        for line in nf:
            group_pat = re.search('((?<=^\[).*(?=\]))', line)
            if group_pat:
                cur_gr = group_pat.group(1)
            if cur_gr == targ_group:
                key_pat = re.search('(^[^=]+)\=(.*$)', line)
                if key_pat:
                    new_dict[key_pat.group(1)] = key_pat.group(2)
    finally:
        nf.close()
    return new_dict
        

Ardis_kw = {}
Ardis_kw['name'] = 'Ardis_test'
Ardis_kw['dir'] = 'Ardis_test'
Ardis_kw['vers'] = '0.6'
Ardis_kw['comment'] = 'Simple and flat icon theme with long shadow - v'+Ardis_kw['vers']
Ardis_kw['path'] = find_theme_path(Ardis_kw['dir'])

AB_rc_dict = parse_file(os.path.join(Ardis_kw['path'], "index.theme"), 'X-ArdisBuilder Settings')
Ardis_index_dict = parse_file(os.path.join(Ardis_kw['path'], "index.theme"), 'Icon Theme')
del Ardis_index_dict['Directories']

ardis_vers_pat = re.search('((?<= \- v).*)', Ardis_index_dict['Comment'])
if ardis_vers_pat:
    Ardis_kw['vers'] = ardis_vers_pat.group(1)
    
Ardis_kw['edition'] = AB_rc_dict.get('Edition')
print Ardis_kw['vers']
if Ardis_kw['edition'] is None:
    AB_rc_dict['Edition'] = 'Basic'
    Ardis_kw['edition'] = 'Basic'

ardis_unlocked_places = ['Blue', 'Violet', 'Brown']
ardis_unlocked_statuses = ['Standard Type', 'Light icons with no background']
ardis_unlocked_categories = ['Standard Type', 'Standard type\nwith gray background']
ardis_unlocked_apps = ['Standard Type', 'Standard type\nwith gray background']

AB_Pages = {0: dict(desc='intro', viewport='viewport1', has_radios=False), 1: dict(desc='actions', viewport='viewport2', has_radios=True, rad_box='box7', lab_box='box5', img_box='box6', cur_rad='event_box_curr_radio1'), 2: dict(desc='places', viewport='viewport3', has_radios=True, rad_box='box11', lab_box='box12', img_box='box13', cur_rad='event_box_curr_radio2'), 11: dict(desc='mimetypes', viewport='viewport4', has_radios=False), 3: dict(desc='start-here', viewport='viewport5', has_radios=True, rad_box='box16', lab_box='box17', img_box='box18', cur_rad='event_box_curr_radio4'), 4: dict(desc='DE', viewport='viewport6', has_radios=True, rad_box='box21', lab_box='box22', img_box='box23', cur_rad='event_box_curr_radio5'), 6: dict(desc='thank-you', viewport='viewport7', has_radios=False), 5: dict(desc='categories', viewport='viewport8', has_radios=True, rad_box='box32', lab_box='box33', img_box='box34', cur_rad='event_box_curr_radio3')}

def default_AB_strings():
    newdict = {}
    newdict['Standard Type'] = 'standard'
    newdict['Standard type\nwith gray background'] = 'grayBG'
    newdict['Dark icons with no background'] = 'gray'
    newdict['Light icons with no background'] = 'white'
    return newdict
    
def invert_dict(s_dict):
    n_dict = {}
    for k, v in s_dict.items():
        n_dict[v] = k
    return n_dict

Ardis_colors = {}
Ardis_colors = {'Blackish':'#111111', 'Blue':'#0078ad', 'Brown':'#b59a6e', 'Green':'#85d075', 'Dark Green':'#66ae4a', 'Light Green':'#79c843', 'Olive Green':'#669966', 'Orange':'#f38725', 'Peach':'#ef6a47', 'Pink':'#e65177', 'Red':'#cd1d31', 'Shadow Grey':'#666666', 'Sky Blue':'#6788cc', 'Soft Red':'#b93d48', 'Violet':'#924565', 'Yellow':'#ffcc67'}
Ardis_actions = default_AB_strings()
Ardis_apps = default_AB_strings()
Ardis_status = default_AB_strings()
Ardis_categories = default_AB_strings()


def set_AB_image(ob_id, ob_fname):
    targ_img = builder.get_object(ob_id)
    targ_img.clear()
    targ_img.set_from_file(ob_fname)
    return None
    
def set_AB_image_all(imagedict):
    for i, f in imagedict.items():
        set_AB_image(i, f)

def Ardis_Edition_Apply(edition):
    Ardis_Plus_Images = {}
    Ardis_Plus_Images['image53'] = 'Images/style_light_apps_no_bg.png'
    Ardis_Plus_Images['image26'] = 'Images/places_sample_Red.png'
    Ardis_Plus_Images['image21'] = 'Images/places_sample_Green.png'
    Ardis_Plus_Images['image49'] = 'Images/style_dark_status_no_bg.png'
    Ardis_Plus_Images['image51'] = 'Images/style_light_categories_withno_bg.png'
    intro_text = builder.get_object('label51')
    ye_old_intro_string = intro_text.get_label()
    old_intro_string = re.sub('<b>Ardis Theme Version</b>', '<b>'+Ardis_kw['vers']+'</b>', ye_old_intro_string)
    print old_intro_string
    
    if edition == 'Plus':
        ardis_unlocked_places.append('Red')
        ardis_unlocked_places.append('Green')
        ardis_unlocked_statuses.append('Dark icons with no background')
        ardis_unlocked_categories.append('Light icons with no background')
        ardis_unlocked_apps.append('Light icons with no background')
        
        set_AB_image_all(Ardis_Plus_Images)
        
        new_intro_string = re.sub('Ardis Basic', 'Ardis Plus', old_intro_string)
        intro_text.set_label(str(new_intro_string))
    elif edition == 'Master':
        set_AB_image_all(Ardis_Plus_Images)
        new_intro_string = re.sub('Ardis Basic', 'Ardis Master', old_intro_string)
        intro_text.set_label(str(new_intro_string))
    else:
        intro_text.set_label(str(old_intro_string))

def ardis_dirs(**ArdisDirArgs):
    for k, v in ArdisDirArgs.items():
        AB_rc_dict[k] = v
    themecontexts = ['actions', 'animations', 'apps', 'categories', 'devices', 'emblems', 'emotes', 'intl', 'mimetypes', 'panel', 'places', 'status']
    themedirlist = []
    theme_size_dirs = []
    theme_size_dirs = glob.glob(Ardis_kw['path']+'/*x*/')
    theme_size_dirs.sort()
    for s_dir in theme_size_dirs:
        for c_dir in themecontexts:
            test_s_c_dir = os.path.join(s_dir, c_dir)
            if os.path.isdir(test_s_c_dir):
                theme_ready_path = os.path.relpath(test_s_c_dir, Ardis_kw['path'])
                themedirlist.append(re.sub('\/$', '', theme_ready_path))
                # The index is now happy, now we need to make any needed symlinks
            if os.path.islink(test_s_c_dir):
                try:
                    link_target = 'extra/'+c_dir+'/'+ArdisDirArgs[c_dir]+'/'
                    if os.path.isdir(os.path.join(s_dir, link_target)):
                        os.unlink(test_s_c_dir)
                        os.symlink(link_target, test_s_c_dir)
                        os.utime(test_s_c_dir, None)
                    else:
                        print "Hmm. Looks like "+os.path.join(s_dir, link_target)+" doesnt exist."
                except KeyError, undef_cat:
                    print '***Oops! ', undef_cat, ' is not defined!***' 
    temp_directories = re.sub("\'\,\s\'", ",", str(themedirlist))
    newdirectories = re.sub("(^\[\'|\'\]$)", "", temp_directories)
    return newdirectories

def Hide_Page(p_num_to_hide):
    winbox = builder.get_object("box2")
    #vp_to_hide = p_num_to_hide+1
    #vp_str_to_hide = str(vp_to_hide)
    page_dict = {}
    page_dict = AB_Pages[p_num_to_hide]
    old_vp = builder.get_object(page_dict['viewport'])
    if nextbutton.get_label() == '  Next   ':
        winbox.remove(old_vp)
    
def Show_page(p_num_to_show):
    winbox = builder.get_object("box2")
    vp_to_show = p_num_to_show+1
    #vp_str_to_show = str(vp_to_show)
    #new_vp = builder.get_object('viewport'+vp_str_to_show)
    page_dict = {}
    try:
        page_dict = AB_Pages[p_num_to_show]
    except KeyError, nullpage:
        page_dict = {'viewport': 'viewport99'}
    new_vp = builder.get_object(page_dict['viewport'])
    
    label_choice_page1 = getNthChildLabel('box5', getPosInParent('event_box_curr_radio1'))
    
    label_choice_page2 = getNthChildLabel('box12', getPosInParent('event_box_curr_radio2'))
    
    label_choice_page4 = getNthChildLabel('box17', getPosInParent('event_box_curr_radio4'))

    label_choice_page5 = getNthChildLabel('box22', getPosInParent('event_box_curr_radio5'))
    
    label_choice_page6 = getNthChildLabel('box33', getPosInParent('event_box_curr_radio3'))
    

    
    #this REALLY is now ignored, in favor of the find_theme_path method and Ardis_kw['path']
    if user_DE == 'KDE':
        user_icon_dir = str(user_home_dir+'/.kde/share/icons/')
    elif user_DE is not None:
        user_icon_dir = str(user_home_dir+'/.icons/')
    else:
        user_icon_dir = None
        
    if p_num_to_show >= 6:
    #This is when the last page is triggered
        res_label_obj = builder.get_object('results_summary')
        res_sum = str('<b>Action style=</b>'+label_choice_page1+'''\n<b>Places color=</b>'''+Ardis_colors[label_choice_page2]+'"'+label_choice_page2+'"'+'''\n<b>Small Apps=</b>'''+label_choice_page4+'''\n<b>Status=</b>'''+label_choice_page5+'''\n<b>DesktopEnvironment=</b>'''+user_DE+'''\n<b>Install Location=</b>'''+Ardis_kw['path'])
        res_label_obj.set_markup(res_sum)
        d_string = ardis_dirs(places=label_choice_page2.lower(), actions=Ardis_actions[label_choice_page1], apps=Ardis_apps[label_choice_page4], status=Ardis_status[label_choice_page5], categories=Ardis_categories[label_choice_page6], devices=Ardis_apps[label_choice_page4])
        ardis_d_list = Theme_Indexer.list_from_string(',', d_string)
        dir_len = len(ardis_d_list)
        prog_step = float('1.0') / float(dir_len)
        prog_bar = builder.get_object('progressbar1')
        prog_bar.set_fraction(float('0.00'))
        
    if p_num_to_show == 6:
        nextbutton.set_label('  Build   ')
        winbox.add(new_vp)
        setPosInParent('curr_page_dot', p_num_to_show)

            
    elif nextbutton.get_label() == '  Build   ':
        #The user has chosen to generate
        
        #First we re-read all the choices
        d_string = ardis_dirs(places=label_choice_page2.lower(), actions=Ardis_actions[label_choice_page1], apps=Ardis_apps[label_choice_page4], status=Ardis_status[label_choice_page5], categories=Ardis_categories[label_choice_page6], devices=Ardis_apps[label_choice_page4])
        ardis_d_list = Theme_Indexer.list_from_string(',', d_string)
        
        #Initialize the progress bar
        dir_len = len(ardis_d_list)
        prog_step = float('1.0') / float(dir_len)
        prog_bar = builder.get_object('progressbar1')
        prog_bar.set_fraction(float('0.00'))
        
        #Start generating the temp theme
        temp_theme_file = open(Ardis_kw['path']+"/temp_index.theme",'w')
        try:
            temp_theme_file.write('Directories='+d_string+'\n\n')
            temp_theme_file.write('[X-ArdisBuilder Settings]\n')
            for k, v in AB_rc_dict.items():
                temp_theme_file.write(k+'='+v+'\n')
            temp_theme_file.write('\n')
            for g_item in ardis_d_list[::]:
                g_line = Theme_Indexer.define_group(g_item)
                temp_theme_file.write(g_line+'\n')
                
                #Now this item of the list is done so we update the progress bar
                old_prog = prog_bar.get_fraction()
                new_prog = old_prog + prog_step
                prog_bar.set_fraction(new_prog)
        finally:
            temp_theme_file.close()
        nextbutton.set_label('  Apply   ')
        
    else:
    #The requested page is just a page (or the end)
        try:
            winbox.add(new_vp)
            setPosInParent('curr_page_dot', p_num_to_show)

        except TypeError:
            #This captures any attempt to advance to a page that doesnt exist
            
            print 'Action style='+'"'+label_choice_page1+'"'
            #print 'Places color='+Ardis_colors[label_choice_page2], '"'+label_choice_page2+'"'
            print 'Places color='+Ardis_colors[label_choice_page2], '"'+label_choice_page2+'"'
            print 'Start here='+label_choice_page4
            print 'DesktopEnvironment='+user_DE
            print 'Install Location='+Ardis_kw['path']
            
            #Apply the temp theme to theme index
            temp_theme_file = open(Ardis_kw['path']+"/temp_index.theme",'r')
            final_theme_file = open(Ardis_kw['path']+"/index.theme",'w')
            try:
                final_theme_file.write('[Icon Theme]\n')
                for k, v in Ardis_index_dict.items():
                    final_theme_file.write(k+'='+v)
                    final_theme_file.write('\n')
                for line in temp_theme_file:
                    final_theme_file.write(line)
            finally:
                temp_theme_file.close()
                final_theme_file.close()
            
            #Politely Trigger updates
            os.utime(Ardis_kw['path'], None)
            theme = Gtk.IconTheme()
            theme.set_custom_theme(Ardis_kw['dir'])
            theme.rescan_if_needed()
            theme.set_custom_theme(None)
            
            #Now Rudely erase KDEs icon cache
            kiconcaches = glob.glob('/var/tmp/kdecache-*/icon-cache.kcache')
            for kde_cache in kiconcaches:
                os.remove(kde_cache)
                print '***CLEARED KDE ICON CACHE "'+kde_cache+'"***'
            
            
            Gtk.main_quit()
            exit()
            
        setPosInParent('curr_page_dot', p_num_to_show)
        if p_num_to_show == 0:
            backbutton.hide()
        else:
            backbutton.show()
    

class Handler:

    def on_window1_delete_event(self, arg1, arg2):
        #Captures exit request made by a window manager
        #Disabling this means closing the window leaves a ZOMBIE!!!
        Gtk.main_quit()
        exit()

    def on_Next_clicked(self, button):
        cur_page = getPosInParent('curr_page_dot')
        nex_page = cur_page+1
        Hide_Page(cur_page)
        Show_page(nex_page)
        #if the next page doesnt exist, the app exits now
        setPosInParent('curr_page_dot', nex_page)
      
    def on_Back_clicked(self, button):
        nextbutton.set_label('  Next   ')
        cur_page = getPosInParent('curr_page_dot')
        prev_page = cur_page-1
        Hide_Page(cur_page)
        Show_page(prev_page)
        setPosInParent('curr_page_dot', prev_page)


    def on_Exit_clicked(self, button):
        exit()
        
    def on_eventbox_radio_press(self, radio, button2):
        cur_page = getPosInParent('curr_page_dot')
        page_dict = AB_Pages[cur_page]
        active_radio_box = builder.get_object(page_dict['cur_rad'])
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
    
def setPosInParent(targ_obj, targ_pos):
    target_object = builder.get_object(targ_obj)
    taget_container = target_object.get_parent()
    taget_container.reorder_child(target_object, targ_pos)
    
    
def getPosInCont(targ_obj, targ_con):
    target_object = builder.get_object(targ_obj)
    taget_container = builder.get_object(targ_con)
    objects_list = taget_container.get_children()
    return objects_list.index(target_object)

def getPosInParent(targ_obj):
    target_object = builder.get_object(targ_obj)
    taget_container = target_object.get_parent()
    objects_list = taget_container.get_children()
    return objects_list.index(target_object)
    
def getNthChildLabel(targ_con, child_n):
    taget_container = builder.get_object(targ_con)
    objects_list = taget_container.get_children()
    target_label = objects_list[child_n]
    return target_label.get_text()

def hide_bonus_choices(unlocked_dict, targ_x):
    targ_parent = builder.get_object(targ_x)
    out_list = []
    col_list = targ_parent.get_children()
    r_list = col_list[0].get_children()
    l_list = col_list[1].get_children()
    p_list = col_list[2].get_children()
    for i, v in enumerate(l_list):
        if v.get_text() not in unlocked_dict:
            out_list.append(r_list[i])
            out_list.append(p_list[i])
            out_list.append(l_list[i])
    for i in out_list:
        i.hide()
        


builder = Gtk.Builder()
builder.add_from_file(w_path+'/Ardis setup unified2.glade')


Ardis_Edition_Apply(Ardis_kw['edition'])


window = builder.get_object("window1")
pageDot = builder.get_object("curr_page_dot")
mainbox = builder.get_object("box1")
nextbutton = builder.get_object("button1")
backbutton = builder.get_object("button2")
pageone = builder.get_object("viewport1")
hide_bonus_choices(ardis_unlocked_places, 'box10')
hide_bonus_choices(ardis_unlocked_statuses, 'box20')
hide_bonus_choices(ardis_unlocked_categories, 'box31')
hide_bonus_choices(ardis_unlocked_apps, 'box15')
current_page = 0
builder.connect_signals(Handler())
window.show_all()
backbutton.hide()
#pageone.show()
gtksettings = Gtk.Settings.get_default()
gtksettings.props.gtk_button_images = True


Gtk.main()
exit()
