__author__ = 'ethan'
import re
import os.path
import cStringIO
import cProfile
import glob


def iter_file_lines(fp):
    assert os.path.isfile(fp)
    with open(fp, 'r') as fd:
        for line in fd:
            yield line

def iter_str_lines(s1):
    assert isinstance(s1, str)
    for line in s1.splitlines():
        yield line


class IniFile(object):
    g_pat = re.compile('((?<=^\[).*(?=\]))')
    k_pat = re.compile('(^[^=]+)\=(.*$)')

    def __init__(self, root_dict):
        assert isinstance(root_dict, dict)
        self.root_dict = root_dict

    @classmethod
    def parse_fbuffer(cls, filebuf):
        groups_dict = {}
        new_list = []
        cur_gr = None
        for line in filebuf:
            group_m = cls.g_pat.search(line)
            if group_m:
                if len(new_list) > 0 and cur_gr:
                    groups_dict[cur_gr] = dict(new_list)
                cur_gr = group_m.group(1)
                new_list = []

            key_m = cls.k_pat.search(line)
            k, v = key_m.groups() if key_m else (None, None)
            if k:
                new_list.append((k, v))
        if len(new_list) > 0 and cur_gr:
            groups_dict[cur_gr] = dict(new_list)

        return groups_dict

    @classmethod
    def from_file(cls, filepath):
        return IniFile(cls.parse_fbuffer(iter_file_lines(filepath)))

    @classmethod
    def from_string(cls, s2):
        return IniFile(cls.parse_fbuffer(iter_str_lines(s2)))

    def to_string1(self):
        def group_str(g_n):
            _gd = self.root_dict[g_n]
            return "[%s]\n%s\n" % (g_n, "\n".join(sorted_items(_gd, "=")))

        def sorted_items(in_dict, joiner=None):
            assert isinstance(in_dict, dict)
            for _k in sorted(in_dict.keys()):
                if joiner:
                    assert isinstance(joiner, str)
                    yield joiner.join((_k, in_dict[_k]))
                else:
                    yield _k, in_dict[_k]

        return "\n".join(map(group_str, self.groups))

    def to_string2(self):
        sbuf = cStringIO.StringIO()
        for _gn in self.groups:
            sbuf.write("[%s]\n" % _gn)
            sbuf.writelines(["=".join((k, self.root_dict[_gn][k] + "\n")) for k in sorted(self.root_dict[_gn].keys())])
            sbuf.write("\n")

        result = sbuf.getvalue()
        sbuf.close()
        return result

    def to_string3(self):
        sbuf = cStringIO.StringIO()
        for _gn in self.groups:
            _gd = self.root_dict[_gn]
            sbuf.write("[%s]\n" % _gn)
            sbuf.writelines(["=".join((k, _gd[k] + "\n")) for k in sorted(_gd.keys())])
            sbuf.write("\n")

        result = sbuf.getvalue()
        sbuf.close()
        return result

    def to_string4(self):
        sbuf = cStringIO.StringIO()
        for _gn in self.groups:
            _gd = self.root_dict[_gn]
            sbuf.write("[%s]\n" % _gn)
            sbuf.writelines([(k + "=" + _gd[k] + "\n") for k in sorted(_gd.keys())])
            sbuf.write("\n")

        result = sbuf.getvalue()
        sbuf.close()
        return result

    def to_string5(self):
        sbuf = cStringIO.StringIO()
        for _gn in self.groups:
            _gd = self.root_dict[_gn]
            sbuf.write("[%s]\n" % _gn)
            sbuf.writelines([("%s=%s\n" % (k, _gd[k])) for k in sorted(_gd.keys())])
            sbuf.write("\n")

        result = sbuf.getvalue()
        sbuf.close()
        return result

    @property
    def groups(self):
        return sorted(self.root_dict.keys())

def sorted_dict_items(d):
    assert isinstance(d, dict)
    return sorted(d.items(), key=lambda itm: itm[0])

def map_index_to_dict(path, verbose=False):
    """
Recursively reads a theme index file, and obeys the index to find all sizes for any given icon.
Organizes this information into a dict with Contexts as top-level keys, icon names as second-level keys, and
a list containing the sizes of the icon, stored as the value of the icon name keys.
    :param path: path to index file
    :param verbose: whether to print the index
    :rtype : dict
    """
    index_file = os.path.join(path, "index.theme")
    ini_dict = IniFile.from_file(index_file).root_dict
    new_dict = ini_dict['Icon Theme']
    index_dict = {}
    if verbose is True:
        print IniFile({'Icon Theme': new_dict}).to_string5()

    for i in ini_dict['Icon Theme']['Directories'].split(','):
        d_dict = ini_dict[i]
        cntxt = d_dict['Context']

        if not index_dict.get(cntxt):
            index_dict[cntxt] = {}

        for fullpath in glob.iglob("%s/*" % os.path.join(path, i)):
            filename = os.path.relpath(fullpath, os.path.join(path, i)).partition('.')[0]

            if not index_dict[cntxt].get(filename):
                index_dict[cntxt][filename] = []

            index_dict[cntxt][filename].append(d_dict['Size'])
    return index_dict


def test():
    tf1 = IniFile.from_file('/Users/ethan/Library/Preferences/KDE/share/config/kdeglobals')
    cProfile.runctx('tf1.to_string1()', globals=globals(), locals=locals())
    cProfile.runctx('tf1.to_string2()', globals=globals(), locals=locals())
    cProfile.runctx('tf1.to_string3()', globals=globals(), locals=locals())
    cProfile.runctx('tf1.to_string4()', globals=globals(), locals=locals())
    cProfile.runctx('tf1.to_string5()', globals=globals(), locals=locals())
    #print tf1.to_string1()
    #print "=" * 50
    #print tf1.to_string2()
    #print tf1.to_string5()

if __name__ == '__main__':
    test()
