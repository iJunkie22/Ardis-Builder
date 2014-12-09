#!/usr/bin/python2.7
# coding: utf-8

import os
import sys
import re
import glob
import subprocess
import shlex
from io import StringIO
from time import sleep



mypath = __file__
assert isinstance(mypath, str)
os.chdir(os.path.dirname(mypath))


class ArdisThemeGen:
    def __init__(self):
        self.rgb_color = dict(r=0, g=0, b=0)
        self.hexdigits = "0123456789ABCDEF"
        self.dec_rep = 0
        self.counter = 0

    def start_shell(self):
        self.args = str("xargs echo $@")
        self.args = "while read line; do (${line}); done"
        self.args = "xargs exec ($@)"
        self.test = subprocess.Popen(self.args, stdin=subprocess.PIPE, shell=True)

    def hex_to_dec(self, hex_str, step=2):
        """
Iterates over hex string with a step of 2 by default, converting to base 10 and yielding each step's result.
        :param hex_str: string
        """
        counter = 1
        old_num = 0
        for i in hex_str.upper():
            cur_num = int(self.hexdigits.index(i))

            if divmod(counter, step)[1] == 0:
                yield int(old_num + cur_num)
                old_num = 0
            else:
                old_num = ((old_num + cur_num) * 16)

            counter += 1

    def set_color_from_hex(self, new_color):
        assert isinstance(new_color, str)
        if new_color[0] == "#":
            new_color = new_color[1::]
        self.dec_rep = list(self.hex_to_dec(new_color, step=6))[0]
        rgb_tuple = tuple(self.hex_to_dec(new_color))
        self.rgb_color["r"], self.rgb_color["g"], self.rgb_color["b"] = rgb_tuple

    @property
    def rgb_str(self):
        """
Returns catenated rgb representation of rgb_color dict.

        :return: str
        """
        return 'rgb(%s,%s,%s)' % (self.rgb_color["r"], self.rgb_color["g"], self.rgb_color["b"])

    def imagemagick_str(self, infile, outfile):
        return "convert '%s' +level-colors ,'%s' '%s'" % (infile, self.rgb_str, outfile)

    def set_color_from_gdk_str(self, new_color):
        new_color_str = new_color[4::][0:-1]
        new_color_list = new_color_str.split(",")
        self.rgb_color["r"], self.rgb_color["g"], self.rgb_color["b"] = new_color_list
        self.dec_rep = "custom"

    def theme_folder_list(self, path, dirs=False, files=False):
        checked_dirs = list()
        for folder_path in glob.iglob("%s/*/extra/actions/white/*" % path):
            dir_tuple = folder_path.rpartition("/white/")
            a, b, c = dir_tuple
            if a not in checked_dirs:
                checked_dirs.append(a)
                if os.path.isdir("%s/%s/" % (a, str(self.dec_rep))) is False:
                    if dirs is True:
                        yield 'mkdir %s/%s' % (a, str(self.dec_rep))
            if files is True:
                yield self.imagemagick_str(folder_path, "%s/%s/%s" % (a, str(self.dec_rep), c))

    def generate(self, input_command):
        self.test = subprocess.Popen(input_command, shell=True)
        self.test.wait()
        self.counter += 1
        x, y = divmod(int(self.counter), 50)
        if y == 0:
            print "%s items done" % self.counter


class ArdisDict:
    def __init__(self):
        self.unlocked = dict(places=['Blue', 'Violet', 'Brown'],
                             actions=['Standard Type', 'Dark icons with no background'],
                             statuses=['Standard Type', 'Light icons with no background'],
                             categories=['Standard Type', 'Standard type\nwith gray background'],
                             apps=['Standard Type', 'Standard type\nwith gray background']
                             )

        self.labels = {'Standard Type': 'standard',
                       'Standard type\nwith gray background': 'grayBG',
                       'Dark icons with no background': 'gray',
                       'Light icons with no background': 'white',
                       'Custom': 'custom'
                       }

        self.images = dict(plus=dict(image53='Images/style_light_apps_no_bg.png',
                                     image26='Images/places_sample_Red.png',
                                     image21='Images/places_sample_Green.png',
                                     image49='Images/style_dark_status_no_bg.png',
                                     image51='Images/style_light_categories_withno_bg.png'
                                     ),
                           mega=dict(image18='Images/places_sample_Black.png',
                                     image23='Images/places_sample_Orange.png',
                                     image27='Images/places_sample_Gray.png',
                                     image39='Images/places_sample_Cyan.png',
                                     image56='Images/style_dark_apps_withno_bg.png',
                                     image58='Images/style_dark_status_icons.png'
                                     )
                           )
        self.image_sets = []
        self.ye_old_intro_string = None

    def apply_unlocks(self, edition):
        ed_level = [None, 'Basic', 'Plus', 'Mega'].index(edition)

        if ed_level > 1:
            self.unlocked['places'].append('Red')
            self.unlocked['places'].append('Green')
            self.unlocked['statuses'].append('Dark icons with no background')
            self.unlocked['categories'].append('Light icons with no background')
            self.unlocked['apps'].append('Light icons with no background')
            self.unlocked['actions'].append('Light icons with no background')
            self.image_sets.append('plus')
        if ed_level > 2:
            self.unlocked['places'].append('Cyan')
            self.unlocked['places'].append('Orange')
            self.unlocked['places'].append('Gray')
            self.unlocked['places'].append('Black')
            self.unlocked['actions'].append('Standard type\nwith gray background')
            self.unlocked['actions'].append('Custom')
            self.unlocked['apps'].append('Dark icons with no background')
            self.unlocked['statuses'].append('Standard type\nwith gray background')
            self.image_sets.append('mega')

    def refresh_unlocked_icons(self, gtkbuilder):
        for i_set in self.image_sets:
            for k, v in self.images[i_set].items():
                obj = gtkbuilder.get_object(k)
                obj.clear()
                obj.set_from_file(v)
        return True

    def apply_edition_labels(self, gtkbuilder, edition=None, vers=None, theme="Ardis"):
        ed_level = [None, 'Basic', 'Plus', 'Mega'].index(edition)

        def replace_intro(self, gtkbuilder, edition):
            intro_lbl_obj = gtkbuilder.get_object('label51')
            new_intro_string = re.sub('Ardis Basic', 'Ardis Plus', old_intro_string)

        outro_text = gtkbuilder.get_object('label46')
        outro = (str('<span>Thank You for choosing %s!</span>\n\n' % theme) +
                 str('<span>%s gives you what others can\'t, it gives you what you deserve,' % theme) +
                 str(' a power of customization.</span>\n\n')
                 )
        intro_text = gtkbuilder.get_object('label51')
        if self.ye_old_intro_string is None:
            self.ye_old_intro_string = intro_text.get_label()
        if vers:
            old_intro_string = re.sub('<b>Ardis Theme Version</b>', '<b>%s</b>' % vers,
                                      self.ye_old_intro_string)
        else:
            old_intro_string = self.ye_old_intro_string

        if ed_level == 2:
            new_intro_string = re.sub('Ardis Basic', '%s Plus' % theme, old_intro_string)
            outro += ('<span>If you think that there\'s not enough customization options for you,'
                      ' and you want more,\n' +
                      str('check other version of %s Icon Theme here:</span>\n\n' % theme) +
                      '  <a href=\"http://kotusworks.wordpress.com/artwork/' +
                      str('%s-icon-theme/#%s_mega\">' % (theme.lower(), theme.lower())) +
                      str(theme + ' Mega Icon Theme</a>\n\n') +
                      str('Thank you for purchasing the Plus version, you contribution means a lot to us.\n\n')
                      )
            intro_text.set_label(str(new_intro_string))
        if ed_level == 3:
            new_intro_string = re.sub('Ardis Basic', '%s Mega' % theme, old_intro_string)

            outro += ('Thank you for purchasing our premium version of our icon theme.\n\n'
                      'Contributions like yours help us to expand this project, and it allows '
                      'us to make many more awesome things in the future!\n\n'
                      )
            intro_text.set_label(str(new_intro_string))
        if ed_level <= 1:
            outro += ('<span>If you think that there\'s not enough customization options for you,'
                      ' and you want more,\n' +
                      str('check other versions of %s Icon Theme here:</span>\n\n' % theme) +
                      str('  <a href=\"http://kotusworks.wordpress.com/artwork/%s-icon-theme/#%s_plus\">' %
                          (theme.lower(), theme.lower())) +
                      str('%s Plus Icon Theme</a>\n\n' % theme) +
                      str('  <a href=\"http://kotusworks.wordpress.com/artwork/%s-icon-theme/#%s_mega\">' %
                          (theme.lower(), theme.lower())) +
                      str('%s Mega Icon Theme</a>\n\n' % theme) +
                      str('By purchasing one of the paid versions of %s, ' % theme) +
                      'you allow us to further develop this project!\n'
                      )
        outro_text.set_label(outro)


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

        self.Ardis_kw = dict(name=None,
                             dir=None,
                             vers='1.0',
                             comment=None,
                             path=None
                             )

        if "--override" in sys.argv:
            for item in sys.argv:
                parts = item.split("=")
                if len(parts) == 2:
                    k, v = parts[0], parts[1]
                    if k in self.Ardis_kw.keys():
                        self.Ardis_kw[k] = v
                        print parts, "override used"

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

        self.load_index_to_dict(self.Ardis_kw['path'])

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
        self.AB_rc_dict = dict()
        self.Ardis_index_dict = dict()

        for k, v in self.AB_Pages.items():
            if v['has_radios'] is True:
                self.choices[v['desc']] = {'label_box': v['lab_box'], 'radio': v['cur_rad']}

    def load_index_to_dict(self, path, keepdirs=False):
        """
Reads the ArdisBuilder settings and Icon Theme settings from an index file to self. Returns True if successful.
        :rtype : bool
        """
        if path is None:
            return False
        self.AB_rc_dict = self.parse_file(os.path.join(path, "index.theme"),
                                          'X-ArdisBuilder Settings')
        self.Ardis_index_dict = self.parse_file(os.path.join(path, "index.theme"), 'Icon Theme')
        self.Ardis_kw['dcount'] = len(self.Ardis_index_dict['Directories'].split(','))
        if keepdirs is False:
            del self.Ardis_index_dict['Directories']

        ardis_vers_pat = re.search('((?<= \- v).*)', self.Ardis_index_dict['Comment'])
        if ardis_vers_pat:
            self.Ardis_kw['vers'] = ardis_vers_pat.group(1)

        self.Ardis_kw['edition'] = self.AB_rc_dict.get('Edition')
        if self.Ardis_kw['edition'] is None:
            self.AB_rc_dict['Edition'] = 'Basic'
            self.Ardis_kw['edition'] = 'Basic'
        return True

    def expose_kde_theme_to_gtk(self, path):
        """
This will let gtk see non-standard icon theme paths, such as those used by kde, by making symlinks.
        :rtype : bool
        """
        ardis_theme_parent = str(os.path.dirname(path))
        # gtk_theme_paths = []
        gtk_real_theme_paths = []
        gtk_def_theme = Gtk.IconTheme.get_default()
        gtk_theme_paths = gtk_def_theme.get_search_path()
        if ardis_theme_parent not in gtk_theme_paths:
            for p in gtk_theme_paths:
                gtk_real_theme_paths.append(os.path.realpath(p))
            if ardis_theme_parent not in gtk_real_theme_paths:
                os.symlink(ardis_theme_parent, os.path.expanduser('~/.local/share/icons'))
            return True
        # End of icon theme path exposer
        return False

    def parse_file(self, indexfile, targ_group):
        """
Selectively reads a specific group in a standard config file into a dict object.

        :param indexfile: path to config file
        :param targ_group: group str
        :rtype : dict
        """
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

    def find_theme_path(self, themedir=None, showall=False):
        icon_theme_locs = []
        searched_locs = []
        themes_here = []
        if self.user_DE == 'KDE':
            icon_theme_locs.append(os.path.expanduser('~/.kde/share/icons'))
            icon_theme_locs.append(os.path.expanduser('~/.kde4/share/icons'))

        elif self.mac_patch is True:
            icon_theme_locs.append(os.path.expanduser('~/Library/Preferences/KDE/share/icons'))

        icon_theme_locs.append(os.path.expanduser('~/.icons'))
        icon_theme_locs.append(self.root_shared_icons_dir)

        for themes_d in icon_theme_locs:

            if os.path.isdir(themes_d):
                for item in os.listdir(themes_d):
                    if os.path.isdir(os.path.join(themes_d, item)):
                        match = re.search("(Ardis|Ursa)", item, flags=re.IGNORECASE)
                        if match:
                            if themedir is None and showall is False:
                                return os.path.join(themes_d, item)
                            themes_here.append(os.path.join(themes_d, item))
            if "--debug" in sys.argv:
                print "--> Found these themes %s" % themes_here
            if themedir:
                pos_theme_path = os.path.join(themes_d, themedir)
                searched_locs.append(pos_theme_path)
                if os.path.isdir(pos_theme_path) and showall is False:
                    return pos_theme_path
        if showall is True:
            if len(themes_here) == 1:
                return themes_here[0]
            if len(themes_here) > 1:
                return themes_here
        print 'Could not find the Ardis theme in any of these locations:'
        for p in searched_locs:
            print p
        print 'exiting...'
        sys.exit(1)

    def map_index_to_dict(self, path, verbose=False):
        """
Recursively reads a theme index file, and obeys the index to find all sizes for any given icon.
Organizes this information into a dict with Contexts as top-level keys, icon names as second-level keys, and
a list containing the sizes of the icon, stored as the value of the icon name keys.
        :param path: path to index file
        :param verbose: whether to print the index
        :rtype : dict
        """
        index_file = os.path.join(path, "index.theme")
        new_dict = self.parse_file(index_file, 'Icon Theme')
        index_dict = dict()
        if verbose is True:
            print "[Icon Theme]"
            for k, v in new_dict.items():
                print "%s=%s" % (k, v)
        for i in new_dict['Directories'].split(','):
            d_dict = self.parse_file(index_file, i)
            if d_dict['Context'] not in index_dict.keys():
                index_dict[d_dict['Context']] = dict()

            for fullpath in glob.iglob("%s/*" % os.path.join(path, i)):
                filename = os.path.relpath(fullpath, os.path.join(path, i)).split('.')[0]
                if filename not in index_dict[d_dict['Context']].keys():
                    index_dict[d_dict['Context']][filename] = list()
                index_dict[d_dict['Context']][filename].append(d_dict['Size'])
        return index_dict

    def default_ab_strings(self):
        """
Acts as a starting point for the ArdisBuilder-to-theme-directory translation dicts.
        :rtype : dict
        """
        newdict = dict()
        newdict['Standard Type'] = 'standard'
        newdict['Standard type\nwith gray background'] = 'grayBG'
        newdict['Dark icons with no background'] = 'gray'
        newdict['Light icons with no background'] = 'white'
        newdict['Custom'] = 'custom'
        return newdict

    def invert_dict(self, s_dict):
        n_dict = {}
        for k, v in s_dict.items():
            n_dict[v] = k
        return n_dict

    def set_ab_image(self, ob_id, ob_fname):
        """

        :rtype : None
        """
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

    def ardis_dirs(self, path, **ArdisDirArgs):
        """


        :param path: theme path
        :param ArdisDirArgs: AB theme settings for each context
        :rtype : str
        """
        self.errorlist = []
        self.errordict = {}
        for k, v in ArdisDirArgs.items():
            self.AB_rc_dict[k] = v
        themecontexts = ['actions', 'animations', 'apps', 'categories', 'devices', 'emblems', 'emotes', 'intl',
                         'mimetypes', 'panel', 'places', 'status']
        themedirlist = []
        theme_size_dirs = []
        theme_size_dirs = glob.glob('%s/*x*/' % path)
        theme_size_dirs.sort()
        for s_dir in theme_size_dirs:
            for c_dir in themecontexts:
                test_s_c_dir = os.path.join(s_dir, c_dir)
                if os.path.isdir(test_s_c_dir):
                    theme_ready_path = os.path.relpath(test_s_c_dir, path)
                    themedirlist.append(re.sub('\/$', '', theme_ready_path))
                    # The index is now happy, now we need to make any needed symlinks
                if os.path.islink(test_s_c_dir):
                    if "--debug" in sys.argv:
                        print "-->ardis_dirs-->Found symlink %s" % test_s_c_dir
                    try:
                        link_target = 'extra/' + c_dir + '/' + ArdisDirArgs[c_dir] + '/'
                        if os.path.isdir(os.path.join(s_dir, link_target)):
                            os.unlink(test_s_c_dir)
                            os.symlink(link_target, test_s_c_dir)
                            os.utime(test_s_c_dir, None)
                        else:
                            new_sym_error = str(
                                "Hmm. Looks like %s doesnt exist." % os.path.join(s_dir, link_target))
                            if "--debug" in sys.argv:
                                print "-->ardis_dirs-->%s" % new_sym_error
                            self.errorlist.append(new_sym_error)
                            self.errordict[theme_ready_path] = dict(SymLinkError=str(os.path.join(s_dir, link_target)))
                    except KeyError, undef_cat:
                        new_cat_error = str('***Oops! %s is not defined!***' % str(undef_cat))
                        if "--debug" in sys.argv:
                            print "-->ardis_dirs-->%s" % new_cat_error
                        self.errordict[theme_ready_path]['UndefinedCategoryError'] = str(undef_cat)
                        self.errorlist.append(new_cat_error)
        if "--debug" in sys.argv:
            print "-->ardis_dirs-->%s" % str(self.errordict)
            print "-->ardis_dirs-->%s" % str(self.errorlist)
        temp_directories = re.sub("\'\,\s\'", ",", str(themedirlist))
        newdirectories = re.sub("(^\[\'|\'\]$)", "", temp_directories)
        return newdirectories

    def hide_page(self, p_num_to_hide):
        winbox = builder.get_object("box2")
        page_dict = {}
        page_dict = self.AB_Pages[p_num_to_hide]
        assert isinstance(page_dict, dict)
        assert isinstance(page_dict['viewport'], str)

        old_vp = builder.get_object(page_dict['viewport'])
        if nextbutton.get_label() == '  Next   ':
            winbox.remove(old_vp)

    def show_page(self, p_num_to_show):
        winbox = builder.get_object("box2")
        vp_to_show = p_num_to_show + 1
        completeness = ''
        try:
            page_dict = self.AB_Pages[p_num_to_show]
        except KeyError, nullpage:
            page_dict = {'viewport': 'viewport99'}
        assert isinstance(page_dict, dict)
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
            d_string = self.ardis_dirs(self.Ardis_kw['path'],
                                       places=self.choice_values['places'].lower(),
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
        #splash_win.show_all()
        #sleep(1)
        #splash_win.hide()
        #window.show_all
        self.combobox = builder.get_object('comboboxtext1')
        if len(abapp.find_theme_path('Ardis', showall=True)) > 1:
            for i in abapp.find_theme_path('Ardis', showall=True):
                self.combobox.append_text(str(i))
            picker_win.show_all()
            #This will call the prompt
        else:
            abapp.load_index_to_dict(abapp.find_theme_path())
            self.on_splash_show(hidden=True)

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

    def on_splash_mapped(self, *args):
        #print "hi"
        #splash_box.show_now()
        #splash_prog_lbl.show_now()
        #sleep(3)
        pass

    def start_spinner(self, *args):
        #gen_spinner.start()
        self.on_gen_colorized()
        #self.stop_spinner()
        return None

    def stop_spinner(self, *args):
        gen_spinner.stop()
        return None

    def on_gen_colorized(self, *args):
        for result in custom_color_gen.theme_folder_list(abapp.Ardis_kw['path'], dirs=True):
            custom_color_gen.generate(result)
        for result2 in custom_color_gen.theme_folder_list(abapp.Ardis_kw['path'], files=True):
            custom_color_gen.generate(result2)
        gen_lbl.show()
        return None

    def on_splash_lbl_drawn(self, *args):
        print "drawn"

    def on_picker_submit_clicked(self, *args):
        choice = self.combobox.get_active_text()
        if choice:
            abapp.Ardis_kw['path'] = choice
            abapp.Ardis_kw['dir'] = os.path.basename(choice)
            picker_win.hide()
            self.on_splash_show(hidden=False)

    def on_splash_show(self, hidden=False, *args):
        #print "drawn2"
        if hidden is False:
            splash_win.show_all()
        if hidden is True:
            splash_win.hide()
        splash_prog_lbl = builder.get_object('splash_prog_lbl')
        splash_progbar = builder.get_object('splash_progbar')
        splash_prog_lbl.props.label = "Reading theme index into memory"
        abapp.load_index_to_dict(abapp.Ardis_kw['path'])

        splash_progbar.set_fraction(0.1)

        splash_prog_lbl.props.label = "Reading edition-specific properties"
        theme_dict.apply_unlocks(abapp.Ardis_kw['edition'])
        #theme_dict.apply_unlocks(abapp.AB_rc_dict['Edition'])
        splash_progbar.set_fraction(0.2)

        splash_prog_lbl.props.label = "Loading additional preview icons"
        theme_dict.refresh_unlocked_icons(builder)
        splash_progbar.set_fraction(0.3)

        splash_prog_lbl.props.label = "Hiding Locked Items"
        hide_bonus_choices(theme_dict.unlocked['places'], 'box10')
        splash_progbar.set_fraction(0.4)
        hide_bonus_choices(theme_dict.unlocked['statuses'], 'box20')
        splash_progbar.set_fraction(0.5)
        hide_bonus_choices(theme_dict.unlocked['categories'], 'box31')
        splash_progbar.set_fraction(0.6)
        hide_bonus_choices(theme_dict.unlocked['apps'], 'box15')
        splash_progbar.set_fraction(0.7)
        hide_bonus_choices(theme_dict.unlocked['actions'], 'box3')
        splash_progbar.set_fraction(0.8)
        #theme_dict.refresh_unlocked_icons(builder)
        theme_dict.apply_edition_labels(builder, abapp.AB_rc_dict['Edition'], theme=abapp.Ardis_kw['dir'])
        splash_progbar.set_fraction(1.0)
        if "--debug" not in sys.argv:
            splash_win.hide()
            window.show_all()
            backbutton.hide()
            #extrastuffbutton.hide()
            return False
        print "done"
        #sleep(3)
        print "woken"
        print Gtk.main_level()
        print splash_prog_lbl.props.label
        for prop in dir(splash_prog_lbl.props):
            try:
                print "\n", prop
                print splash_prog_lbl.props.__getattribute__(str(prop))
            except AttributeError:
                pass
            except TypeError:
                pass
        splash_win.hide()
        window.show_all()

    def on_splash_lbl_realized(self, *args):
        #print "realized"
        #sleep(1)
        pass

    def moo(self, *args):
        print "moo"

    def remap(self, *args):
        print args
        #obj.unmap()

        #obj.map()
        print "unmapping"
        args[0].unmap()
        print "remapping"
        args[0].map()
        print "remapped"
        return True

    def reset_buffer(self, buffer):
        buffer.set_text("")

    def on_extras_btn_click(self, button):
        combo_box_theme = builder.get_object('comboboxtext2')
        text_buffer = builder.get_object('textbuffer2')
        if button.props.name == "print_self_index":
            theme_choice = combo_box_theme.get_active_text()
            oxy_theme_path = abapp.find_theme_path(themedir=theme_choice, showall=False)
            if oxy_theme_path is None:
                return False

            ardis_dict = abapp.map_index_to_dict(abapp.Ardis_kw['path'], verbose=False)
            oxygen_dict = abapp.map_index_to_dict(oxy_theme_path, verbose=False)

            dif_dict1 = oxygen_dict
            for c, c_dict in oxygen_dict.items():
                if c in ardis_dict.keys():
                    for f_n, f_list in c_dict.items():
                        if f_n in ardis_dict[c].keys():
                            for s in f_list:
                                if s in ardis_dict[c][f_n]:
                                    dif_dict1[c][f_n].remove(s)

            read_mapped_index(dif_dict1, buffer=text_buffer)

            return True
        else:
            return False

    def print_event(self, *args):
        if "--debug" not in sys.argv:
            return None
        print args, "hi"
        event = args[1]
        try:
            #print dir(event)
            print event.get_event_type()
        except AttributeError:
            pass
        print ""

    def on_splash_lbl_show(self, *args):
        print "shown"
        #sleep(1)

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
        """

        :rtype : bool
        """
        wind.hide_on_delete()
        if wind.props.title == 'Password':
            self.pw_purpose = self.old_pw_purpose
        return True
        # print self.get_active()

    def on_color_chosen(self, widget, prop):
        color_btn = builder.get_object("action_color_btn")
        new_color = widget.props.rgba
        for i in color_btn.get_children():
            i.override_background_color(0, new_color)
        color_str = widget.props.rgba.to_string()
        custom_color_gen.set_color_from_gdk_str(color_str)
        gen_lbl.hide()


    def on_eventbox_radio_press(self, radio, void):
        """

        :param radio: Gtk.EventBox
        :param void: null
        """
        rad_parent = radio.get_parent()
        rad_siblings = rad_parent.get_children()
        i = int(rad_siblings.index(radio))

        if "--debug" in sys.argv:
            rad_grammy = rad_parent.get_parent()
            rad_uncles = rad_grammy.get_children()
            lbl_siblings = rad_uncles[1].get_children()

            rad_pos = int(list(c.props.name for c in rad_siblings).index('cur_rad'))
            try:
                chosen = str(list(abapp.Ardis_generic[x.props.label] for x in lbl_siblings)[i])
            except KeyError, e:
                chosen = str(list(x.props.label for x in lbl_siblings)[i])
            finally:
                print chosen

        cur_dict = abapp.AB_Pages[self.cur_page]
        assert isinstance(cur_dict, dict)
        cur_rad = builder.get_object(cur_dict["cur_rad"])
        rad_parent.reorder_child(cur_rad, i)

    def on_open_window_clicked(self, window3, *junk):
        window3.show_all()

        theme_dict.apply_edition_labels(builder, "Mega", theme="Ardis")
        if window3.props.title == 'Password':
            pathstat = os.stat(os.path.join(abapp.Ardis_kw['path'], 'index.theme'))
            builder.get_object('lbl_cur_u_num').props.label = str(os.getuid())
            builder.get_object('lbl_cur_o_num').props.label = str(pathstat.st_uid)

    def on_pw_submit_clicked(self, text_entry):
        if self.pw_purpose == "Unlock permissions of root-installed Ardis":
            args = str("sudo -kS chmod -v -R a+rw '%s'" % abapp.Ardis_kw['path'])
            print args
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
    output = list(target_object.get_parent().get_children()).index(target_object)
    return output


def getNthChildLabel(targ_con, child_n):
    taget_container = builder.get_object(targ_con)
    output = taget_container.get_children()[child_n].get_text()
    return output


def hide_bonus_choices(unlocked_dict, targ_x):
    targ_parent = builder.get_object(targ_x)
    out_list = []
    col_list = targ_parent.get_children()
    for i, v in enumerate(list(z.get_text() for z in col_list[1].get_children())):

        if v not in unlocked_dict:
            out_list.extend(list(x.get_children()[i] for x in col_list))
    for obj in out_list:
        obj.hide()


def read_mapped_index(mapped_dict, buffer=None):
    for k, v in mapped_dict.items():
        if buffer:
            buffer.insert_at_cursor(str("\n\n\n[%s]\n" % k))
        else:
            print "\n\n\n[%s]" % k
        for a in sorted(v.keys()):
            temp_directories = re.sub("\'\,\s\'", ",", str(v[a]))
            item_directories = re.sub("(^\[\'|\'\]$)", "", temp_directories)
            if buffer:
                buffer.insert_at_cursor(str("%s=%s\n" % (a, item_directories)))
            else:
                print "%s=%s" % (a, item_directories)



__warningregistry__ = dict()
abapp = ArdisBuilder()

import gi
from gi.repository import Gtk
from gi.repository import Gdk
import Theme_Indexer

builder = Gtk.Builder()
builder.add_from_file(abapp.w_path + '/Ardis setup unified2.glade')

theme_dict = ArdisDict()
#abapp.ardis_edition_apply(abapp.Ardis_kw['edition'])
custom_color_gen = ArdisThemeGen()

window = builder.get_object("window1")
splash_win = builder.get_object("AB_splash_window")
picker_win = builder.get_object('picker')
advsetwin = builder.get_object("window2")
pageDot = builder.get_object("curr_page_dot")
mainbox = builder.get_object("box1")
nextbutton = builder.get_object("button1")
backbutton = builder.get_object("button2")
aboutbutton = builder.get_object("box38")
extrastuffbutton = builder.get_object("box37")
pageone = builder.get_object("viewport1")
gen_spinner = builder.get_object("spinner1")
gen_lbl = builder.get_object("lbl_gen_status")



#hide_bonus_choices(abapp.ardis_unlocked_places, 'box10')
#hide_bonus_choices(abapp.ardis_unlocked_statuses, 'box20')
#hide_bonus_choices(abapp.ardis_unlocked_categories, 'box31')
#hide_bonus_choices(abapp.ardis_unlocked_apps, 'box15')
#hide_bonus_choices(abapp.ardis_unlocked_actions, 'box3')
current_page = 0
builder.connect_signals(Handler())

ssh_session = abapp.envars.get('SSH_CONNECTION')
#splash_win.show_now()
builder.get_object('splash_prog_lbl').show_now()
builder.get_object('splash_progbar').show_now()
#sleep(2)

splash_prog_lbl = builder.get_object('splash_prog_lbl')
splash_progbar = builder.get_object('splash_progbar')
splash_box = builder.get_object('AB_splash_rootbox')


if ssh_session:
    pass
    # exit()
blah = Gtk.main()

exit()
