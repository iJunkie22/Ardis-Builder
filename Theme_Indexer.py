import re
import string

class ThemeIndex:
    def __init__(self):
        self.smart_pattern = re.compile(r'(((?P<size>[0-9]+)x(?P=size))/(?P<context>(actions|animations|apps|categories|devices|emblems|emotes|intl|mimetypes|places|status)))')
        self.name = ''
        self.comment = ''
        self.inherits = ''
        self.directories = ''
        self.directory_list = []
        self.hidden = False
        self.Settings = {}
    def add_dir_to_list(self, new_dir):
        self.directory_list.append(new_dir)
    
    def update_dirs_string(self):
        self.temp_directories = re.sub("\'\,\s\'", ",", str(self.directory_list))
        self.directories = re.sub("(^\[\'|\'\]$)", "", self.temp_directories)
        self.temp_directories = None
        
    def parse_config_string(self, c_str):
        name_pat = re.search('((?<=^Name\=).*)', c_str)
        if name_pat:
            self.name = name_pat.group(1)
        comm_pat = re.search('((?<=^Comment\=).*)', c_str)
        if comm_pat:
            self.comment = comm_pat.group(1)
                
                
    
    def dump_theme(self):
        return "[Icon Theme]\nName="+self.name+"\nComment="+self.comment+"\nDirectories="+self.directories+"\n"
        
context_dict = {'actions':'Actions', 'apps':'Applications', 'categories':'Categories', 'devices':'Devices','mimetypes':'MimeTypes','panel':'Panel', 'places':'Places','status':'Status'}

def define_group(g_path):
    header = str('['+g_path+']')
    dir_parts = re.split('\/', g_path)
    type_t = 'Type=Scalable'
    size_d = 'Size='+dir_parts[0]
    size_t = re.search('([0-9]+$)', size_d)
    if size_t:
        size_d = 'Size='+size_t.group(0)
        type_t = 'Type=Threshold'
    else:
        size_d = 'Size=512'
        
    cont_d = dir_parts[1]
    cont_t = 'Context='+context_dict[cont_d]
    try:
        style_d = dir_parts[2]
        return header+'\n'+size_d+'\n'+cont_t+'\n'+type_t+'\n'
    except IndexError:
        style_d = None
        return header+'\n'+cont_t+'\n'+type_t+'\n'+size_d+'\n'

def smart_define_group(g_path):
    header = str('['+g_path+']')
    g_re = re.match(r'(((?P<size>[0-9]+)x(?P=size))/(?P<context>(actions|animations|apps|categories|devices|emblems|emotes|intl|mimetypes|places|status)))', g_path)
    dir_parts = re.split('\/', g_path)
    type_t = 'Type=Scalable'
    size_d = 'Size='+dir_parts[0]
    size_t = re.search('([0-9]+$)', size_d)
    if size_t:
        size_d = 'Size='+size_t.group(0)
        type_t = 'Type=Threshold'
    else:
        size_d = 'Size=512'
        
    cont_d = dir_parts[1]
    cont_t = 'Context='+context_dict[cont_d]
    try:
        style_d = dir_parts[2]
        return header+'\n'+size_d+'\n'+cont_t+'\n'+type_t+'\n'
    except IndexError:
        style_d = None
        return header+'\n'+cont_t+'\n'+type_t+'\n'+size_d+'\n'

def sample_string(null):
    sample = '16x16/apps/standard,16x16/devices,16x16/categories,16x16/actions/standard,16x16/mimetypes,16x16/places/violet,16x16/status,22x22/apps/standard,22x22/devices,22x22/categories,22x22/actions/standard,22x22/mimetypes,22x22/places/violet,22x22/status,22x22/panel,24x24/apps/standard,24x24/devices,24x24/categories,24x24/actions/standard,24x24/mimetypes,24x24/places/violet,24x24/panel,24x24/status,32x32/apps,32x32/devices,32x32/categories,32x32/actions/standard,32x32/mimetypes,32x32/places/violet,32x32/status,48x48/apps,48x48/devices,48x48/categories,48x48/actions/standard,48x48/mimetypes,48x48/places/violet,48x48/status,64x64/apps,64x64/devices,64x64/categories,64x64/actions/standard,64x64/mimetypes,64x64/places/violet,64x64/status,96x96/apps,96x96/devices,96x96/categories,96x96/actions/standard,96x96/mimetypes,96x96/places/violet,96x96/status,128x128/apps,128x128/devices,128x128/categories,128x128/mimetypes,128x128/places/violet,128x128/status,scalable/apps,scalable/devices,scalable/categories,scalable/actions/standard,scalable/mimetypes,scalable/places/violet,scalable/status'
    return sample

def list_from_string(d_splitter, d_set):
    return re.split(d_splitter, d_set)


