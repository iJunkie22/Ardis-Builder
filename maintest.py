#!/usr/bin/python2.7
#coding: utf-8

import os
import sys
import re
import glob

mac_patch = False
if sys.platform == 'darwin':
    print 'MacPorts patch ACTIVATED'
    sys.path.append('/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')
    mac_patch = True
    root_shared_icons_dir = '/opt/local/share/icons'
else:
    root_shared_icons_dir = '/usr/share/icons'
    
import gi
gi.require_version('Gtk', '3.0')
# Credit for this patch goes to https://build.opensuse.org/package/view_file/openSUSE:12.3/alacarte/alacarte-force-Gtk3.patch?expand=1
from gi.repository import Gtk

w_path = os.getcwd()
sys.path.append(str(w_path))
import Theme_Indexer


m_list = []
m_list = sys.modules.keys()
if "gi" not in m_list:
    print sys.prefix
    print sys.exec_prefix
    print '='*30
    print "Search Paths >>>>"
    for p_i in sys.path:
        print p_i
    print '='*30
    print 'Module List >>>>', m_list
    sys.path.append('/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')
    exit()
else:
    pass

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
        

envars = {}
GDM_dict = {}
user_GDMS = None
envars = os.environ.copy()
user_home_dir = envars['HOME']
user_DE = envars.get('XDG_CURRENT_DESKTOP')
if user_DE is None:
    # The GDM doesnt declare the fairly new (added ~2014) XDG_CURRENT_DESKTOP global...
    user_GDMS = envars.get('GDMSESSION')
    if user_GDMS:
        GDM_dict = parse_file('/usr/share/xsessions/'+user_GDMS+'.desktop', 'Desktop Entry')
        if GDM_dict['Type'] == 'XSession':
            # This is probably a valid session description file
            user_DE = GDM_dict['DesktopNames']
    elif mac_patch == True:
        user_DE = 'N/A(Using XQuartz on OSX)'
    else:
        user_DE = 'unknown'

def find_theme_path(themedir):
    icon_theme_locs = []
    searched_locs = []
    if user_DE == 'KDE':
        icon_theme_locs.append(os.path.expanduser('~/.kde/share/icons'))
        icon_theme_locs.append(os.path.expanduser('~/.kde4/share/icons'))
        icon_theme_locs.append(os.path.expanduser('~/.icons'))
    else:
        icon_theme_locs.append(os.path.expanduser('~/.icons'))
        
    icon_theme_locs.append(root_shared_icons_dir)
    
    for themes_d in icon_theme_locs:
        pos_theme_path = os.path.join(themes_d, themedir)
        searched_locs.append(pos_theme_path)
        if os.path.isdir(pos_theme_path):
            return pos_theme_path
            break
    print 'Could not find the Ardis theme in any of these locations:'
    for p in searched_locs:
        print p
    print 'exiting...'
    sys.exit(1)


Ardis_kw = {}
Ardis_kw['name'] = 'Ardis_test'
Ardis_kw['dir'] = 'Ardis_test'
Ardis_kw['vers'] = '0.6'
Ardis_kw['comment'] = 'Simple and flat icon theme with long shadow - v'+Ardis_kw['vers']
Ardis_kw['path'] = find_theme_path(Ardis_kw['dir'])


# This will let gtk see non-standard icon theme paths, such as those used by kde
ardis_theme_parent = str(os.path.dirname(Ardis_kw['path']))
gtk_theme_paths = []
gtk_real_theme_paths = []
gtk_def_theme = Gtk.IconTheme.get_default()
gtk_theme_paths = gtk_def_theme.get_search_path()
if ardis_theme_parent not in gtk_theme_paths:
    for p in gtk_theme_paths:
        gtk_real_theme_paths.append(os.path.realpath(p))
    if ardis_theme_parent not in gtk_real_theme_paths:
        os.symlink(ardis_theme_parent, os.path.expanduser('~/.local/share/icons'))
# End of icon theme path exposer

AB_rc_dict = parse_file(os.path.join(Ardis_kw['path'], "index.theme"), 'X-ArdisBuilder Settings')
Ardis_index_dict = parse_file(os.path.join(Ardis_kw['path'], "index.theme"), 'Icon Theme')
Ardis_kw['dcount'] = len(Ardis_index_dict['Directories'].split(','))
del Ardis_index_dict['Directories']


ardis_vers_pat = re.search('((?<= \- v).*)', Ardis_index_dict['Comment'])
if ardis_vers_pat:
    Ardis_kw['vers'] = ardis_vers_pat.group(1)
    
Ardis_kw['edition'] = AB_rc_dict.get('Edition')
if Ardis_kw['edition'] is None:
    AB_rc_dict['Edition'] = 'Basic'
    Ardis_kw['edition'] = 'Basic'

ardis_unlocked_places = ['Blue', 'Violet', 'Brown']
ardis_unlocked_actions = ['Standard Type', 'Dark icons with no background']
ardis_unlocked_statuses = ['Standard Type', 'Light icons with no background']
ardis_unlocked_categories = ['Standard Type', 'Standard type\nwith gray background']
ardis_unlocked_apps = ['Standard Type', 'Standard type\nwith gray background']

AB_Pages = {0: dict(desc='intro', viewport='viewport1', has_radios=False), 1: dict(desc='actions', viewport='viewport2', has_radios=True, rad_box='box7', lab_box='box5', img_box='box6', cur_rad='event_box_curr_radio1'), 4: dict(desc='places', viewport='viewport3', has_radios=True, rad_box='box11', lab_box='box12', img_box='box13', cur_rad='event_box_curr_radio2'), 11: dict(desc='mimetypes', viewport='viewport4', has_radios=False), 2: dict(desc='small apps', viewport='viewport5', has_radios=True, rad_box='box16', lab_box='box17', img_box='box18', cur_rad='event_box_curr_radio4'), 3: dict(desc='status', viewport='viewport6', has_radios=True, rad_box='box21', lab_box='box22', img_box='box23', cur_rad='event_box_curr_radio5'), 5: dict(desc='thank-you', viewport='viewport7', has_radios=False), 20: dict(desc='categories', viewport='viewport8', has_radios=True, rad_box='box32', lab_box='box33', img_box='box34', cur_rad='event_box_curr_radio3')}

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
Ardis_colors = {'Black':'#111111', 'Blue':'#0078ad', 'Brown':'#b59a6e', 'Green':'#85d075', 'Dark Green':'#66ae4a', 'Light Green':'#79c843', 'Olive Green':'#669966', 'Orange':'#f38725', 'Peach':'#ef6a47', 'Pink':'#e65177', 'Red':'#cd1d31', 'Grey':'#666666', 'Cyan':'#6788cc', 'Soft Red':'#b93d48', 'Violet':'#924565', 'Yellow':'#ffcc67'}
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
    Ardis_Mega_Images = {}
    Ardis_Plus_Images['image53'] = 'Images/style_light_apps_no_bg.png'
    Ardis_Plus_Images['image26'] = 'Images/places_sample_Red.png'
    Ardis_Plus_Images['image21'] = 'Images/places_sample_Green.png'
    Ardis_Plus_Images['image49'] = 'Images/style_dark_status_no_bg.png'
    Ardis_Plus_Images['image51'] = 'Images/style_light_categories_withno_bg.png'
    intro_text = builder.get_object('label51')
    ye_old_intro_string = intro_text.get_label()
    old_intro_string = re.sub('<b>Ardis Theme Version</b>', '<b>'+Ardis_kw['vers']+'</b>', ye_old_intro_string)
    
    if edition == 'Plus' or edition == 'Mega':
        ardis_unlocked_places.append('Red')
        ardis_unlocked_places.append('Green')
        ardis_unlocked_statuses.append('Dark icons with no background')
        ardis_unlocked_categories.append('Light icons with no background')
        ardis_unlocked_apps.append('Light icons with no background')
        ardis_unlocked_actions.append('Light icons with no background')

        set_AB_image_all(Ardis_Plus_Images)
        
        if edition == 'Plus':
            new_intro_string = re.sub('Ardis Basic', 'Ardis Plus', old_intro_string)

        elif edition == 'Mega':
            ardis_unlocked_places.append('Cyan')
            ardis_unlocked_places.append('Orange')
            ardis_unlocked_places.append('Shadow Grey')
            ardis_unlocked_places.append('Blackish')
            ardis_unlocked_actions.append('Standard type\nwith gray background')
            #ardis_unlocked_actions.append('Custom1')
            #ardis_unlocked_actions.append('Custom2')
            
            Ardis_Mega_Images['image18'] = 'Images/places_sample_Black.png'
            Ardis_Mega_Images['image23'] = 'Images/places_sample_Orange.png'
            Ardis_Mega_Images['image27'] = 'Images/places_sample_Gray.png'
            Ardis_Mega_Images['image39'] = 'Images/places_sample_Cyan.png'


            
            set_AB_image_all(Ardis_Mega_Images)
            
            new_intro_string = re.sub('Ardis Basic', 'Ardis Mega', old_intro_string)
        
        intro_text.set_label(str(new_intro_string))
    else:
        intro_text.set_label(str(old_intro_string))

def ardis_dirs(**ArdisDirArgs):
    errorlist = []
    errordict = {}
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
                        new_sym_error = str("Hmm. Looks like "+os.path.join(s_dir, link_target)+" doesnt exist.")
                        
                        errorlist.append(new_sym_error)
                        errordict[theme_ready_path] = dict(SymLinkError=str(os.path.join(s_dir, link_target)))
                except KeyError, undef_cat:
                    new_cat_error = str('***Oops! ', undef_cat, ' is not defined!***')
                    errordict[theme_ready_path]['UndefinedCategoryError'] = str(undef_cat)
                    errorlist.append(new_cat_error)
    temp_directories = re.sub("\'\,\s\'", ",", str(themedirlist))
    newdirectories = re.sub("(^\[\'|\'\]$)", "", temp_directories)
    return newdirectories, errorlist, errordict

def Hide_Page(p_num_to_hide):
    winbox = builder.get_object("box2")
    page_dict = {}
    page_dict = AB_Pages[p_num_to_hide]
    old_vp = builder.get_object(page_dict['viewport'])
    if nextbutton.get_label() == '  Next   ':
        winbox.remove(old_vp)
    
def Show_page(p_num_to_show):
    winbox = builder.get_object("box2")
    vp_to_show = p_num_to_show+1
    page_dict = {}
    completeness = ''
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
        
    if p_num_to_show >= 5:
    #This is when the last page is triggered
        res_label_obj = builder.get_object('results_summary')
        try:
            res_sum = str('<b>Action style=</b>'+label_choice_page1+'''\n<b>Places color=</b>'''+Ardis_colors[label_choice_page2]+'"'+label_choice_page2+'"'+'''\n<b>Small Apps=</b>'''+label_choice_page4+'''\n<b>Status=</b>'''+label_choice_page5+'''\n<b>DesktopEnvironment=</b>'''+user_DE+'''\n<b>Install Location=</b>'''+Ardis_kw['path'])
        except TypeError, sumerror1:
            res_sum = str(sumerror1)+'error'
        except KeyError, sumerror2:
            #Either the path key and/or the color key is missing
            try:
                #Try reporting without using the color key
                res_sum = str('<b>Action style=</b>'+label_choice_page1+'''\n<b>Places color=</b>'''+'"'+label_choice_page2+'"'+'''\n<b>Small Apps=</b>'''+label_choice_page4+'''\n<b>Status=</b>'''+label_choice_page5+'''\n<b>DesktopEnvironment=</b>'''+user_DE+'''\n<b>Install Location=</b>'''+Ardis_kw['path'])
            except KeyError, sumerror3:
                #The path key is missing. This needs to be a fatal error
                res_sum = str(sumerror3)+'error'
        res_label_obj.set_markup(res_sum)
        dir_len = Ardis_kw['dcount']
        #This alternative method uses the number of directories in the OLD list, since it should be the same anyway
        #avoids the unnecessary calling of ardis_dirs, and the premature application of symlinks
        prog_step = float('1.0') / float(dir_len)
        prog_bar = builder.get_object('progressbar1')
        #prog_bar.text = None
        prog_bar.set_property('text', None)
        prog_bar.set_fraction(float('0.00'))
        
    if p_num_to_show == 5:
        nextbutton.set_label('  Build   ')
        winbox.add(new_vp)
        setPosInParent('curr_page_dot', p_num_to_show)

            
    elif nextbutton.get_label() == '  Build   ':
        #The user has chosen to generate
        
        #First we re-read all the choices
        d_string, AB_e_list, AB_e_dict = ardis_dirs(places=label_choice_page2.lower(), actions=Ardis_actions[label_choice_page1], apps=Ardis_apps[label_choice_page4], status=Ardis_status[label_choice_page5], categories=Ardis_categories[label_choice_page6], devices=Ardis_apps[label_choice_page4])
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
            e_count = 0
            for g_item in ardis_d_list[::]:
                g_line = Theme_Indexer.define_group(g_item)
                temp_theme_file.write(g_line+'\n')
                
                #Now this item of the list is done so we update the progress bar
                old_prog = prog_bar.get_fraction()
                new_prog = old_prog + prog_step
                prog_bar.set_fraction(new_prog)
            #print AB_e_dict.keys()
                if g_item in AB_e_dict.keys():
                    e_count = e_count + 1
                    
                #completeness = str(float(prog_bar.get_fraction()) * float(100))
                if e_count > 0:
                    prog_bar.set_text(completeness+'  completed with '+str(e_count)+' errors')
            for k, v in AB_e_dict.items():
                print k, v
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
            print 'Places color="'+label_choice_page2+'"'
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
            theme.emit('changed')
            theme.rescan_if_needed()
            theme.set_custom_theme(None)
            
            theme2 = Gtk.IconTheme.get_default()
            theme2.emit('changed')
            theme2.rescan_if_needed()
            
            #Now Rudely erase GNOMEs icon cache
            clean_switch_GNOME = builder.get_object('switch2')
            if clean_switch_GNOME.get_active() == True:
                #This part is still experimental, and may not work at all
                giconcaches = glob.glob('/usr/share/icons/gnome/icon-cache.cache')
                for gnome_cache in giconcaches:
                    try:
                        os.remove(gnome_cache)
                        print '***CLEARED GNOME ICON CACHE "'+gnome_cache+'"***'
                    except OSError:
                        pass
                    
            #Now Rudely erase KDEs icon cache
            clean_switch_KDE = builder.get_object('switch1')
            if clean_switch_KDE.get_active() == True:
                kiconcaches = glob.glob('/var/tmp/kdecache-*/icon-cache.kcache')
                for kde_cache in kiconcaches:
                    os.remove(kde_cache)
                    print '***CLEARED KDE ICON CACHE "'+kde_cache+'"***'
            
            
            Gtk.main_quit()
            exit()
            
        #If it made it this far it is normal and safe. YAY!
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
        
    def on_adv_settings_button_press(self, button, evbox):
        advsetwin.show_all()
        
    def on_AdvSettings_toggle(self, tog):
        #this is a simple test to make sure everything is connected
        print tog.get_active()
        
    def hide_adv_settings(self, wind, winbool):
        wind.hide_on_delete()
        return True
        #print self.get_active()
        
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
advsetwin = builder.get_object("window2")
pageDot = builder.get_object("curr_page_dot")
mainbox = builder.get_object("box1")
nextbutton = builder.get_object("button1")
backbutton = builder.get_object("button2")
pageone = builder.get_object("viewport1")
hide_bonus_choices(ardis_unlocked_places, 'box10')
hide_bonus_choices(ardis_unlocked_statuses, 'box20')
hide_bonus_choices(ardis_unlocked_categories, 'box31')
hide_bonus_choices(ardis_unlocked_apps, 'box15')
hide_bonus_choices(ardis_unlocked_actions, 'box3')
current_page = 0
builder.connect_signals(Handler())
window.show_all()
backbutton.hide()
#pageone.show()
gtksettings = Gtk.Settings.get_default()
gtksettings.props.gtk_button_images = True

ssh_session = envars.get('SSH_CONNECTION')
if ssh_session:
    pass
    #exit()
Gtk.main()
exit()
