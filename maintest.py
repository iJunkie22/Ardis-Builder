#!/usr/bin/python2.7
# coding: utf-8

import os
import sys
import re
import glob
import subprocess
import shlex
from io import StringIO


class ArdisBuilder:
    def __init__(self):
        self.mac_patch = False
        if sys.platform == 'darwin':
            print 'MacPorts patch ACTIVATED'
            sys.path.append('/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')
            self.mac_patch = True
            self.root_shared_icons_dir = '/opt/local/share/icons'
        else:
            self.root_shared_icons_dir = '/usr/share/icons'

        import gi

        gi.require_version('Gtk', '3.0')
        # Credit for this patch goes to
        # https://build.opensuse.org/package/view_file/openSUSE:12.3/alacarte/alacarte-force-Gtk3.patch?expand=1
        if self.mac_patch is True:
            from gi.overrides.Gtk import Gtk
            from gi.overrides.Gdk import Gdk
        else:
            from gi.repository import Gtk
            from gi.repository import Gdk

        self.w_path = os.getcwd()
        sys.path.append(str(self.w_path))

        # envars = {}
        self.GDM_dict = dict()
        self.user_GDMS = None
        self.envars = os.environ.copy()
        self.user_home_dir = self.envars['HOME']
        self.user_DE = self.envars.get('XDG_CURRENT_DESKTOP')
        if self.user_DE is None:
            # The GDM doesnt declare the fairly new (added ~2014) XDG_CURRENT_DESKTOP global...
            self.user_GDMS = self.envars.get('GDMSESSION')
            if self.user_GDMS:
                self.GDM_dict = self.parse_file('/usr/share/xsessions/' + self.user_GDMS + '.desktop', 'Desktop Entry')
                if self.GDM_dict['Type'] == 'XSession':
                    # This is probably a valid session description file
                    self.user_DE = self.GDM_dict['DesktopNames']
            elif self.mac_patch is True:
                self.user_DE = 'N/A(Using XQuartz on OSX)'
            else:
                self.user_DE = 'unknown'

        self.Ardis_kw = dict(name='Ardis',
                             dir='Ardis',
                             vers='1.0',
                             )
        self.Ardis_kw['comment'] = 'Simple and flat icon theme with long shadow - v' + self.Ardis_kw['vers'],
        self.Ardis_kw['path'] = self.find_theme_path(self.Ardis_kw['dir'])

        m_list = sys.modules.keys()
        if "gi" not in m_list:
            # Debugging-related info. If this is triggered, please include it in the report you send :)
            print sys.prefix
            print sys.exec_prefix
            print '=' * 30
            print "Search Paths >>>>"
            for p_i in sys.path:
                print p_i
            print '=' * 30
            print 'Module List >>>>', m_list
            sys.path.append('/opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages')
            exit(1)
        else:
            pass

        # This will let gtk see non-standard icon theme paths, such as those used by kde
        ardis_theme_parent = str(os.path.dirname(self.Ardis_kw['path']))
        # gtk_theme_paths = []
        gtk_real_theme_paths = []
        gtk_def_theme = Gtk.IconTheme.get_default()
        gtk_theme_paths = gtk_def_theme.get_search_path()
        if ardis_theme_parent not in gtk_theme_paths:
            for p in gtk_theme_paths:
                gtk_real_theme_paths.append(os.path.realpath(p))
            if ardis_theme_parent not in gtk_real_theme_paths:
                os.symlink(ardis_theme_parent, os.path.expanduser('~/.local/share/icons'))
        # End of icon theme path exposer

        self.AB_rc_dict = self.parse_file(os.path.join(self.Ardis_kw['path'], "index.theme"),
                                          'X-ArdisBuilder Settings')
        self.Ardis_index_dict = self.parse_file(os.path.join(self.Ardis_kw['path'], "index.theme"), 'Icon Theme')
        self.Ardis_kw['dcount'] = len(self.Ardis_index_dict['Directories'].split(','))
        del self.Ardis_index_dict['Directories']

        ardis_vers_pat = re.search('((?<= \- v).*)', self.Ardis_index_dict['Comment'])
        if ardis_vers_pat:
            self.Ardis_kw['vers'] = ardis_vers_pat.group(1)

        self.Ardis_kw['edition'] = self.AB_rc_dict.get('Edition')
        if self.Ardis_kw['edition'] is None:
            self.AB_rc_dict['Edition'] = 'Basic'
            self.Ardis_kw['edition'] = 'Basic'

        self.ardis_unlocked_places = ['Blue', 'Violet', 'Brown']
        self.ardis_unlocked_actions = ['Standard Type', 'Dark icons with no background']
        self.ardis_unlocked_statuses = ['Standard Type', 'Light icons with no background']
        self.ardis_unlocked_categories = ['Standard Type', 'Standard type\nwith gray background']
        self.ardis_unlocked_apps = ['Standard Type', 'Standard type\nwith gray background']

        self.AB_Pages = {0: dict(desc='intro',
                                 viewport='viewport1',
                                 has_radios=False),
                         1: dict(desc='actions',
                                 viewport='viewport2',
                                 has_radios=True,
                                 rad_box='box7',
                                 lab_box='box5',
                                 img_box='box6',
                                 cur_rad='event_box_curr_radio1'),
                         4: dict(desc='places',
                                 viewport='viewport3',
                                 has_radios=True,
                                 rad_box='box11',
                                 lab_box='box12',
                                 img_box='box13',
                                 cur_rad='event_box_curr_radio2'),
                         11: dict(desc='mimetypes',
                                  viewport='viewport4',
                                  has_radios=False),
                         2: dict(desc='small apps',
                                 viewport='viewport5',
                                 has_radios=True,
                                 rad_box='box16',
                                 lab_box='box17',
                                 img_box='box18',
                                 cur_rad='event_box_curr_radio4'),
                         3: dict(desc='status',
                                 viewport='viewport6',
                                 has_radios=True,
                                 rad_box='box21',
                                 lab_box='box22',
                                 img_box='box23',
                                 cur_rad='event_box_curr_radio5'),
                         5: dict(desc='thank-you',
                                 viewport='viewport7',
                                 has_radios=False),
                         20: dict(desc='categories',
                                  viewport='viewport8',
                                  has_radios=True,
                                  rad_box='box32',
                                  lab_box='box33',
                                  img_box='box34',
                                  cur_rad='event_box_curr_radio3')}
        # Ardis_colors = {}
        self.Ardis_colors = {'Black': '#111111', 'Blue': '#0078ad', 'Brown': '#b59a6e', 'Green': '#85d075',
                             'Dark Green': '#66ae4a', 'Light Green': '#79c843', 'Olive Green': '#669966',
                             'Orange': '#f38725', 'Peach': '#ef6a47', 'Pink': '#e65177', 'Red': '#cd1d31',
                             'Gray': '#666666', 'Cyan': '#6788cc', 'Soft Red': '#b93d48',
                             'Violet': '#924565', 'Yellow': '#ffcc67'}
        self.Ardis_actions = self.default_ab_strings()
        self.Ardis_apps = self.default_ab_strings()
        self.Ardis_status = self.default_ab_strings()
        self.Ardis_categories = self.default_ab_strings()
        self.Ardis_generic = self.default_ab_strings()
        self.choices = dict()
        self.choice_values = dict()

        for k, v in self.AB_Pages.items():
            if v['has_radios'] is True:
                self.choices[v['desc']] = {'label_box': v['lab_box'], 'radio': v['cur_rad']}

    def parse_file(self, indexfile, targ_group):
        new_dict = {}
        nf = open(indexfile, 'r')
        try:
            # new_dict = {}
            cur_gr = ""
            for line in nf:
                group_pat = re.search('((?<=^\[).*(?=\]))', line)
                if group_pat:
                    cur_gr = group_pat.group(1)
                if cur_gr == targ_group:
                    key_pat = re.search('(^[^=]+)=(.*$)', line)
                    if key_pat:
                        new_dict[key_pat.group(1)] = key_pat.group(2)
        finally:
            nf.close()
        return new_dict

    def find_theme_path(self, themedir):
        icon_theme_locs = []
        searched_locs = []
        if self.user_DE == 'KDE':
            icon_theme_locs.append(os.path.expanduser('~/.kde/share/icons'))
            icon_theme_locs.append(os.path.expanduser('~/.kde4/share/icons'))

        elif self.mac_patch is True:
            icon_theme_locs.append(os.path.expanduser('~/Library/Preferences/KDE/share/icons'))

        icon_theme_locs.append(os.path.expanduser('~/.icons'))
        icon_theme_locs.append(self.root_shared_icons_dir)

        for themes_d in icon_theme_locs:
            pos_theme_path = os.path.join(themes_d, themedir)
            searched_locs.append(pos_theme_path)
            if os.path.isdir(pos_theme_path):
                return pos_theme_path
        print 'Could not find the Ardis theme in any of these locations:'
        for p in searched_locs:
            print p
        print 'exiting...'
        sys.exit(1)

    def default_ab_strings(self):
        newdict = dict()
        newdict['Standard Type'] = 'standard'
        newdict['Standard type\nwith gray background'] = 'grayBG'
        newdict['Dark icons with no background'] = 'gray'
        newdict['Light icons with no background'] = 'white'
        return newdict

    def invert_dict(self, s_dict):
        n_dict = {}
        for k, v in s_dict.items():
            n_dict[v] = k
        return n_dict

    def set_ab_image(self, ob_id, ob_fname):
        targ_img = builder.get_object(ob_id)
        targ_img.clear()
        targ_img.set_from_file(ob_fname)
        return None

    def set_ab_image_all(self, imagedict):
        for i, f in imagedict.items():
            self.set_ab_image(i, f)

    def ardis_edition_apply(self, edition):
        global new_intro_string
        outro_text = builder.get_object('label46')
        outro = ('<span>Thank You for chosing Ardis!</span>\n\n'
                 '<span>Ardis gives you what others can\'t, it gives you what you deserve,'
                 ' a power of customization.</span>\n\n'
                 )

        Ardis_Plus_Images = {}
        Ardis_Mega_Images = {}
        Ardis_Plus_Images['image53'] = 'Images/style_light_apps_no_bg.png'
        Ardis_Plus_Images['image26'] = 'Images/places_sample_Red.png'
        Ardis_Plus_Images['image21'] = 'Images/places_sample_Green.png'
        Ardis_Plus_Images['image49'] = 'Images/style_dark_status_no_bg.png'
        Ardis_Plus_Images['image51'] = 'Images/style_light_categories_withno_bg.png'
        intro_text = builder.get_object('label51')
        ye_old_intro_string = intro_text.get_label()
        old_intro_string = re.sub('<b>Ardis Theme Version</b>', '<b>' + self.Ardis_kw['vers'] + '</b>',
                                  ye_old_intro_string)

        if edition == 'Plus' or edition == 'Mega':
            self.ardis_unlocked_places.append('Red')
            self.ardis_unlocked_places.append('Green')
            self.ardis_unlocked_statuses.append('Dark icons with no background')
            self.ardis_unlocked_categories.append('Light icons with no background')
            self.ardis_unlocked_apps.append('Light icons with no background')
            self.ardis_unlocked_actions.append('Light icons with no background')

            self.set_ab_image_all(Ardis_Plus_Images)

            if edition == 'Plus':
                new_intro_string = re.sub('Ardis Basic', 'Ardis Plus', old_intro_string)
                outro += ('<span>If you think that there\'s not enough customization options for you,'
                          ' and you want more,\n'
                          'check other version of Ardis Icon Theme here:</span>\n\n'
                          '  <a href=\"http://kotusworks.wordpress.com/artwork/ardis-icon-theme/#ardis_mega\">'
                          'Ardis Mega Icon Theme</a>\n\n'
                          'Thank you for purchasing the Plus version, you contribution means a lot to us.\n\n'
                          )

            elif edition == 'Mega':
                self.ardis_unlocked_places.append('Cyan')
                self.ardis_unlocked_places.append('Orange')
                self.ardis_unlocked_places.append('Gray')
                self.ardis_unlocked_places.append('Black')
                self.ardis_unlocked_actions.append('Standard type\nwith gray background')
                self.ardis_unlocked_apps.append('Dark icons with no background')
                self.ardis_unlocked_statuses.append('Standard type\nwith gray background')
                # ardis_unlocked_actions.append('Custom1')
                # ardis_unlocked_actions.append('Custom2')

                Ardis_Mega_Images['image18'] = 'Images/places_sample_Black.png'
                Ardis_Mega_Images['image23'] = 'Images/places_sample_Orange.png'
                Ardis_Mega_Images['image27'] = 'Images/places_sample_Gray.png'
                Ardis_Mega_Images['image39'] = 'Images/places_sample_Cyan.png'
                Ardis_Mega_Images['image56'] = 'Images/style_dark_apps_withno_bg.png'
                Ardis_Mega_Images['image58'] = 'Images/style_dark_status_icons.png'

                self.set_ab_image_all(Ardis_Mega_Images)

                new_intro_string = re.sub('Ardis Basic', 'Ardis Mega', old_intro_string)
                outro += ('Thank you for purchasing our premium version of our icon theme.\n\n'
                          'Contributions like yours help us to expand this project, and it allows '
                          'us to make many more awesome things in the future!\n\n'
                          )

            intro_text.set_label(str(new_intro_string))
        else:
            intro_text.set_label(str(old_intro_string))
            outro += ('<span>If you think that there\'s not enough customization options for you,'
                      ' and you want more,\n'
                      'check other versions of Ardis Icon Theme here:</span>\n\n'
                      '  <a href=\"http://kotusworks.wordpress.com/artwork/ardis-icon-theme/#ardis_plus\">'
                      'Ardis Plus Icon Theme</a>\n\n'
                      '  <a href=\"http://kotusworks.wordpress.com/artwork/ardis-icon-theme/#ardis_mega\">'
                      'Ardis Mega Icon Theme</a>\n\n'
                      'By purchasing one of the paid versions of Ardis, you allow us to further develop this project!\n'
                      )

        outro_text.set_label(outro)

    def ardis_dirs(self, **ArdisDirArgs):
        self.errorlist = []
        self.errordict = {}
        for k, v in ArdisDirArgs.items():
            self.AB_rc_dict[k] = v
        themecontexts = ['actions', 'animations', 'apps', 'categories', 'devices', 'emblems', 'emotes', 'intl',
                         'mimetypes', 'panel', 'places', 'status']
        themedirlist = []
        theme_size_dirs = []
        theme_size_dirs = glob.glob(self.Ardis_kw['path'] + '/*x*/')
        theme_size_dirs.sort()
        for s_dir in theme_size_dirs:
            for c_dir in themecontexts:
                test_s_c_dir = os.path.join(s_dir, c_dir)
                if os.path.isdir(test_s_c_dir):
                    theme_ready_path = os.path.relpath(test_s_c_dir, self.Ardis_kw['path'])
                    themedirlist.append(re.sub('\/$', '', theme_ready_path))
                    # The index is now happy, now we need to make any needed symlinks
                if os.path.islink(test_s_c_dir):
                    try:
                        link_target = 'extra/' + c_dir + '/' + ArdisDirArgs[c_dir] + '/'
                        if os.path.isdir(os.path.join(s_dir, link_target)):
                            os.unlink(test_s_c_dir)
                            os.symlink(link_target, test_s_c_dir)
                            os.utime(test_s_c_dir, None)
                        else:
                            new_sym_error = str(
                                "Hmm. Looks like " + os.path.join(s_dir, link_target) + " doesnt exist.")

                            self.errorlist.append(new_sym_error)
                            self.errordict[theme_ready_path] = dict(SymLinkError=str(os.path.join(s_dir, link_target)))
                    except KeyError, undef_cat:
                        new_cat_error = str('***Oops! ' + str(undef_cat) + ' is not defined!***')
                        self.errordict[theme_ready_path]['UndefinedCategoryError'] = str(undef_cat)
                        self.errorlist.append(new_cat_error)
        temp_directories = re.sub("\'\,\s\'", ",", str(themedirlist))
        newdirectories = re.sub("(^\[\'|\'\]$)", "", temp_directories)
        return newdirectories

    def hide_page(self, p_num_to_hide):
        winbox = builder.get_object("box2")
        page_dict = {}
        page_dict = self.AB_Pages[p_num_to_hide]
        old_vp = builder.get_object(page_dict['viewport'])
        if nextbutton.get_label() == '  Next   ':
            winbox.remove(old_vp)

    def show_page(self, p_num_to_show):
        winbox = builder.get_object("box2")
        vp_to_show = p_num_to_show + 1
        page_dict = {}
        completeness = ''
        try:
            page_dict = self.AB_Pages[p_num_to_show]
        except KeyError, nullpage:
            page_dict = {'viewport': 'viewport99'}
        new_vp = builder.get_object(page_dict['viewport'])

        for k, v in self.choices.items():
            if k == 'places':
                self.choice_values[k] = getNthChildLabel(v['label_box'], getPosInParent(v['radio']))
            else:
                self.choice_values[k] = self.Ardis_generic[getNthChildLabel(v['label_box'], getPosInParent(v['radio']))]

        if '--debug' in sys.argv:
            print self.choice_values

        if p_num_to_show >= 5:
            # This is when the last page is triggered
            res_label_obj = builder.get_object('results_summary')
            try:

                res_sum = ('Your selected options are:\n'
                           '  <b>Action icons</b> = {0}\n'
                           '  <b>Folders color</b> = {1}\n'
                           '  <b>Small icons</b> = {2}\n'
                           '  <b>Status icons</b> = {3}\n'
                           ).format(self.choice_values['actions'].title(), self.choice_values['places'],
                                    self.choice_values['small apps'].title(), self.choice_values['status'].title())
                if '--debug' in sys.argv:
                    res_sum = ('{0}'
                               '  <b>DesktopEnvironment=</b>{1}\n'
                               '  <b>Install Location=</b>{2}\n'
                               ).format(res_sum, self.user_DE, self.Ardis_kw['path'])

            except KeyError, sumerror3:
                # The path key is missing. This needs to be a fatal error
                res_sum = str(sumerror3) + 'error'

            res_label_obj.set_markup(res_sum)
            dir_len = self.Ardis_kw['dcount']
            # This alternative method uses the number of directories in the OLD list, since it should be the same anyway
            # avoids the unnecessary calling of ardis_dirs, and the premature application of symlinks
            prog_bar = builder.get_object('progressbar1')
            prog_bar.set_property('text', None)
            prog_bar.set_fraction(float('0.00'))

        if p_num_to_show == 5:
            nextbutton.set_label('  Build   ')
            winbox.add(new_vp)
            setPosInParent('curr_page_dot', p_num_to_show)

        elif nextbutton.get_label() == '  Build   ':
            # The user has chosen to generate
            # First we re-read all the choices
            d_string = self.ardis_dirs(places=self.choice_values['places'].lower(),
                                       actions=self.choice_values['actions'],
                                       apps=self.choice_values['small apps'],
                                       status=self.choice_values['status'],
                                       categories=self.choice_values['categories'],
                                       devices=self.choice_values['small apps'])
            ardis_d_list = Theme_Indexer.list_from_string(',', d_string)
            # Initialize the progress bar
            dir_len = len(ardis_d_list)
            prog_step = float('1.0') / float(dir_len)
            prog_bar = builder.get_object('progressbar1')
            prog_bar.set_fraction(float('0.00'))

            # Start generating the temp theme
            temp_theme_file = open(self.Ardis_kw['path'] + "/temp_index.theme", 'w')
            try:
                temp_theme_file.write('Directories=%s\n\n[X-ArdisBuilder Settings]\n' % d_string)
                for k, v in self.AB_rc_dict.items():
                    temp_theme_file.write(k + '=' + v + '\n')
                temp_theme_file.write('\n')
                e_count = 0
                for g_item in ardis_d_list[::]:
                    g_line = Theme_Indexer.define_group(g_item)
                    temp_theme_file.write(g_line + '\n')

                    # Now this item of the list is done so we update the progress bar
                    old_prog = prog_bar.get_fraction()
                    new_prog = old_prog + prog_step
                    prog_bar.set_fraction(new_prog)
                    # print self.errordict.keys()
                    if g_item in self.errordict.keys():
                        e_count = e_count + 1

                    # completeness = str(float(prog_bar.get_fraction()) * float(100))
                    if e_count > 0:
                        prog_bar.set_text('{0} completed with {1} errors'.format(completeness, str(e_count)))
                for k, v in self.errordict.items():
                    print k, v
            finally:
                temp_theme_file.close()
            nextbutton.set_label('  Apply   ')

        else:
            # The requested page is just a page (or the end)
            try:
                winbox.add(new_vp)
                setPosInParent('curr_page_dot', p_num_to_show)

            except TypeError:
                # This captures any attempt to advance to a page that doesnt exist

                print 'Action style=' + '"' + self.choice_values['actions'] + '"'
                # print 'Places color='+Ardis_colors[self.choice_values['places']], '"'+self.choice_values['places']+'"'
                print 'Places color="' + self.choice_values['places'] + '"'
                print 'Start here=' + self.choice_values['small apps']
                print 'DesktopEnvironment=' + self.user_DE
                print 'Install Location=' + self.Ardis_kw['path']

                # Apply the temp theme to theme index
                temp_theme_file = open(self.Ardis_kw['path'] + "/temp_index.theme", 'r')
                final_theme_file = open(self.Ardis_kw['path'] + "/index.theme", 'w')
                try:
                    final_theme_file.write('[Icon Theme]\n')
                    for k, v in self.Ardis_index_dict.items():
                        final_theme_file.write("{0}={1}\n".format(k, v))
                    for line in temp_theme_file:
                        final_theme_file.write(line)
                finally:
                    temp_theme_file.close()
                    final_theme_file.close()

                # Politely Trigger updates
                os.utime(self.Ardis_kw['path'], None)
                theme = Gtk.IconTheme()
                theme.set_custom_theme(self.Ardis_kw['dir'])
                theme.emit('changed')
                theme.rescan_if_needed()
                theme.set_custom_theme(None)
                try:
                    print Gtk.Settings.props.gtk_icon_theme_name()
                except TypeError:
                    pass

                theme2 = Gtk.IconTheme.get_default()
                theme2.emit('changed')
                theme2.rescan_if_needed()

                if self.mac_patch is True:
                    print "-" * 40
                    print ">>> You will need to apply {0} with: \nkwriteconfig --group Icons --key Theme {0}".format(
                        self.Ardis_kw['name'])
                    print "-" * 40

                # Now Rudely erase GNOMEs icon cache
                clean_switch_GNOME = builder.get_object('switch2')
                if clean_switch_GNOME.get_active() is True:
                    # This part is still experimental, and may not work at all
                    giconcaches = glob.glob('/usr/share/icons/gnome/icon-cache.cache')
                    for gnome_cache in giconcaches:
                        try:
                            os.remove(gnome_cache)
                            print '***CLEARED GNOME ICON CACHE "' + gnome_cache + '"***'
                        except OSError:
                            pass

                # Now Rudely erase KDEs icon cache
                clean_switch_KDE = builder.get_object('switch1')
                if clean_switch_KDE.get_active() is True:
                    kiconcaches = glob.glob('/var/tmp/kdecache-*/icon-cache.kcache')
                    for kde_cache in kiconcaches:
                        os.remove(kde_cache)
                        print '***CLEARED KDE ICON CACHE "' + kde_cache + '"***'

                Gtk.main_quit()
                exit()

            # If it made it this far it is normal and safe. YAY!
            setPosInParent('curr_page_dot', p_num_to_show)
            if p_num_to_show == 0:
                backbutton.hide()
            else:
                backbutton.show()

    def make_desktop_launcher(self):
        #This is still in development
        new_desk_file = StringIO()

        try:
            new_desk_file.write("[Desktop Entry]\nCategories=Settings;")
            for line in new_desk_file:
                print line
        finally:
            new_desk_file.close()
        pass


class Handler:
    def __init__(self):
        window.show_all()
        backbutton.hide()
        aboutbutton.hide()
        extrastuffbutton.hide()
        self.page_dot_dot = builder.get_object('curr_page_dot')
        self.page_dot_container = self.page_dot_dot.get_parent()
        self.cur_page = self.page_dot_container.get_children().index(self.page_dot_dot)
        #self.page_dot_container.child_get_property(self.page_dot_dot, "position", self.cur_page)
        self.nex_page = self.cur_page + 1
        self.prev_page = self.cur_page - 1
        self.pw_purpose = ""
        self.old_pw_purpose = ""
        # pageone.show()
        self.test_var = "moo"
        try:
            self.gtksettings = Gtk.Settings.get_default()
            self.gtksettings.props.gtk_button_images = True
        finally:
            pass

    def on_window1_delete_event(self, arg1, arg2):
        # Captures exit request made by a window manager
        # Disabling this means closing the window leaves a ZOMBIE!!!
        Gtk.main_quit()
        exit()

    def on_Next_clicked(self, button):
        self.cur_page = self.page_dot_container.get_children().index(self.page_dot_dot)
        self.nex_page = self.cur_page + 1
        abapp.hide_page(self.cur_page)
        abapp.show_page(self.nex_page)
        # if the next page doesnt exist, the app exits now
        self.page_dot_container.reorder_child(self.page_dot_dot, self.nex_page)
        self.cur_page = self.page_dot_container.get_children().index(self.page_dot_dot)

    def on_Back_clicked(self, button):
        nextbutton.set_label('  Next   ')
        self.cur_page = self.page_dot_container.get_children().index(self.page_dot_dot)
        self.prev_page = self.cur_page - 1
        abapp.hide_page(self.cur_page)
        abapp.show_page(self.prev_page)
        self.page_dot_container.reorder_child(self.page_dot_dot, self.prev_page)
        self.cur_page = self.page_dot_container.get_children().index(self.page_dot_dot)

    def on_Exit_clicked(self, button):
        exit()

    #def on_adv_settings_button_press(self, button, evbox):
     #   advsetwin.show_all()

    def on_AdvSettings_toggle(self, tog):
        # this is a simple test to make sure everything is connected
        print tog.get_active()

    def hide_adv_settings(self, wind, event):
        wind.hide_on_delete()
        if wind.props.title == 'Password':
            self.pw_purpose = self.old_pw_purpose
        return True
        # print self.get_active()

    def on_eventbox_radio_press(self, radio, image):
        rad_parent = radio.get_parent()
        i = rad_parent.get_children().index(radio)
        cur_rad = builder.get_object(abapp.AB_Pages[self.cur_page]["cur_rad"])
        rad_parent.reorder_child(cur_rad, i)

    def on_open_window_clicked(self, window3, *junk):
        window3.show_all()
        if window3.props.title == 'Password':
            pathstat = os.stat(os.path.join(abapp.Ardis_kw['path'], 'index.theme'))
            builder.get_object('lbl_cur_u_num').props.label = str(os.getuid())
            builder.get_object('lbl_cur_o_num').props.label = str(pathstat.st_uid)

    def on_pw_submit_clicked(self, text_entry):
        if self.pw_purpose == "Unlock permissions of root-installed Ardis":
            args = str("sudo -kS chmod -v -R a+rw " + abapp.Ardis_kw['path'])
        else:
            args = str("xargs echo $@")
        test = subprocess.Popen(args, stdin=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
        stdout, stderr = test.communicate(input=str(text_entry.props.text + "\n"))
        stderr_list = str(stderr).split('\n')
        stderr_list.remove('Password:')
        if '' in stderr_list:
            stderr_list.remove('')

        stderr_label = builder.get_object('pw_stderr_label')
        if len(stderr_list) == 0:
            new_label = "Success!"
            new_color = Gdk.RGBA(red=0, green=1.0, blue=0, alpha=0.5)
        else:
            new_label = "Incorrect Password"
            new_color = Gdk.RGBA(red=1.0, green=0.5, blue=0, alpha=0.5)

        stderr_label.props.label = new_label
        stderr_label.override_background_color(0, new_color)

        pathstat = os.stat(os.path.join(abapp.Ardis_kw['path'], 'index.theme'))
        builder.get_object('lbl_cur_u_num').props.label = str(os.getuid())
        builder.get_object('lbl_cur_o_num').props.label = str(pathstat.st_uid)

    def set_pw_context(self, button):
        self.old_pw_purpose = self.pw_purpose
        self.pw_purpose = button.props.label


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


__warningregistry__ = dict()
abapp = ArdisBuilder()

import gi
from gi.repository import Gtk
from gi.repository import Gdk
import Theme_Indexer

builder = Gtk.Builder()
builder.add_from_file(abapp.w_path + '/Ardis setup unified2.glade')

abapp.ardis_edition_apply(abapp.Ardis_kw['edition'])

window = builder.get_object("window1")
advsetwin = builder.get_object("window2")
pageDot = builder.get_object("curr_page_dot")
mainbox = builder.get_object("box1")
nextbutton = builder.get_object("button1")
backbutton = builder.get_object("button2")
aboutbutton = builder.get_object("box38")
extrastuffbutton = builder.get_object("box37")
pageone = builder.get_object("viewport1")

hide_bonus_choices(abapp.ardis_unlocked_places, 'box10')
hide_bonus_choices(abapp.ardis_unlocked_statuses, 'box20')
hide_bonus_choices(abapp.ardis_unlocked_categories, 'box31')
hide_bonus_choices(abapp.ardis_unlocked_apps, 'box15')
hide_bonus_choices(abapp.ardis_unlocked_actions, 'box3')
current_page = 0
builder.connect_signals(Handler())

ssh_session = abapp.envars.get('SSH_CONNECTION')
if ssh_session:
    pass
    # exit()
Gtk.main()
exit()
