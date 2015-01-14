#!/usr/bin/python2.7
"""
ArdisUtils (C) 2014-2015 Ethan Randall
"""
# coding: utf-8
__author__ = "Ethan Randall"

import re
from optparse import OptionParser
import colorsys


parser = OptionParser()
parser.add_option("-i", "--input",
                  dest="in_filename",
                  default='',
                  help="read report from FILE",
                  metavar="FILE")

parser.add_option("-o", "--output",
                  dest="out_filename",
                  default='',
                  help="write report to FILE",
                  metavar="FILE")

parser.add_option("-q", "--quiet",
                  action="store_false",
                  dest="verbose",
                  default=True,
                  help="don't print status messages")

parser.add_option("-c", "--clean",
                  dest="el_to_clean",
                  help="skip a specific el, such as text")

parser.add_option("-f", "--filters",
                  dest="filters",
                  help="filter using preset, ex: shadows:[hide|hexcolor], white:hexcolor, colorize:[newhex|hide], "
                       "resize:Xpx,Ypx ... can be a ; seperated list")
parser.add_option("-e", "--export",
                  dest="export_filename",
                  help="automatically use imagemagick to convert the outputfile to another as well\nHINT: use this"
                       " with the resize filter for lossless and quick export. Can either be an absolute path with a "
                       "filetype or just a filetype... REMEMBER THE DOT if doing just filetype")


class EmptyClass:
    """
    Acts as a skeleton class.
    """

    def __init__(self):
        pass


class LineProcessor:
    """
    This class encompasses the options and methods ArdisUtils uses for processing(filtering) an SVG document.
    The purpose of this class is to supply python bindings to what was originally a linear command-line utility, and to
    enable the same config to be used multiple times.
    """

    def __init__(self):
        self.colorize_filter = None
        self.shadow_filter = None
        self.resize_filter = None
        self.white_filter = None
        self.el_to_clean = None
        self.filters = None
        self.color_regex = re.compile('('
                                      '((?<=[";]fill:)(#([0-9A-Fa-f]*)([a-eA-E1-9]+)([0-9A-Fa-f]*))(?=[";]))'
                                      '|'
                                      '((?<=[";]stop-color:)(#([0-9A-Fa-f]*)([a-eA-E1-9]+)([0-9A-Fa-f]*))(?=[";]))'
                                      '|'
                                      '(((?<=\sfill=\")(#[0-9A-Fa-f]*)([a-eA-E1-9]+)([0-9A-Fa-f]*))(?=\"))'
                                      '|'
                                      '((((?<=\sstop-color)=\")(#[0-9A-Fa-f]*)([a-eA-E1-9]+)([0-9A-Fa-f]*))(?=\"))'
                                      ')'
                                      )

    def import_options(self, opts_in):
        """
        This method is what allows ArdisUtils to be run from a CLI!
        :param opts_in: Either an instance of OptionParser's options object, or None
        """
        opts = EmptyClass()
        if hasattr(opts_in, "filters") is True and hasattr(opts_in, "el_to_clean") is True:
            opts = opts_in
        if hasattr(opts_in, "filters") is False:
            opts.filters = self.filters
        if hasattr(opts, "filters") is False:
            opts.filters = self.filters
        if hasattr(opts, "el_to_clean") is False:
            opts.el_to_clean = self.el_to_clean

        if opts.el_to_clean:
            self.el_to_clean = opts.el_to_clean

        if opts.filters:
            filters_list = re.split(';', opts.filters)
            for filter_x in filters_list:
                colorize_opt = re.match('colorize:(#?)(hide|[0-9A-Fa-f]+|[0-9A-F]+|#[0-9A-Fa-f]+)', filter_x)
                if colorize_opt:
                    self.colorize_filter = colorize_opt.groups()[-1]
                white_opt = re.match('white:(#?)([0-9A-Fa-f]+)', filter_x)
                if white_opt:
                    self.white_filter = white_opt.groups()[-1]
                shadow_opt = re.match('shadows:(#?)(hide|[0-9A-Fa-f]+)', filter_x)
                if shadow_opt:
                    self.shadow_filter = shadow_opt.groups()[-1]
                resize_opt = re.match('resize:(\d+px),(\d+px)', filter_x)
                if resize_opt:
                    self.resize_filter = dict(width=resize_opt.group(1),
                                              height=resize_opt.group(2)
                    )

    def do_colorize_filter(self, input_line):
        """
        :type input_line: str
        :rtype : str
        """
        if self.colorize_filter is None:
            return input_line
        if self.colorize_filter == 'hide':
            output_line = re.sub(self.color_regex, 'none', input_line)
            return output_line
        else:
            output_line = re.sub(self.color_regex, str(self.colorize_filter), input_line)
            return output_line

    def do_white_filter(self, input_line):
        """
        :type input_line: str
        :rtype : str
        """
        if self.white_filter is None:
            return input_line
        output_line = re.sub('('
                             '((?<=[";]fill:#)([fF]+)(?=[";]))'
                             '|'
                             '((?<=\sfill=\"#)([fF]+)(?=\"))'
                             ')',
                             str(self.white_filter), input_line)
        return output_line

    def do_shadow_filter(self, input_line):
        """
        :type input_line: str
        :rtype : str
        """
        if self.shadow_filter is None:
            return input_line
        match = re.search('opacity:(0\.(2|3)\d*)[";]', input_line)
        if match is None:
            return input_line
        if self.shadow_filter == 'hide':
            output_line = re.sub('opacity:(0\.(2|3)\d*)', 'opacity:0.0', input_line)
            return output_line
        else:
            output_line = re.sub('(((?<=[";]fill:#)(([0-9A-Fa-f]*)([a-eA-E\d]+)[0-9A-Fa-f]*))(?=[";]))',
                                 str(self.shadow_filter), input_line)
            return output_line

    def do_resize_filter(self, input_line):
        """
        :type input_line: str
        :rtype : str
        """
        if self.resize_filter is None:
            return input_line
        resizematch = re.match('\s*(width|height)=\"\d+(em|ex|px|in|cm|mm|pt|pc|%%)?\"', input_line)
        if resizematch:
            size_axis = str(resizematch.group(1))
            output_line = re.sub('((?<==\")(\d+(em|ex|px|in|cm|mm|pt|pc|%%)?)(?=\"))',
                                 self.resize_filter[size_axis], input_line)
            return output_line
        else:
            return input_line

    def loop_over_fp(self, filepath):
        """
        :type filepath: str
        """
        file_in = open(filepath, 'r')
        el_buf = 0
        try:
            for line_in in file_in:
                if self.el_to_clean == "text":
                    m_begin = re.search(r'^\s*<text|^\s*<tspan', line_in)
                    if m_begin:
                        el_buf += 1
                if el_buf == 0:
                    line_filtered = line_in
                    line_filtered = self.do_resize_filter(line_filtered)
                    line_filtered = self.do_shadow_filter(line_filtered)
                    line_filtered = self.do_colorize_filter(line_filtered)
                    line_filtered = self.do_white_filter(line_filtered)
                    yield line_filtered
                else:
                    m_ended = re.search(r'^\s*..text.|.*\s/>', line_in)
                    if m_ended:
                        el_buf -= 1
        finally:
            file_in.close()

    def filter_to_file(self, infile, outfile):
        """
        :type infile: str
        :type outfile: str
        """
        file_out = open(outfile, 'w')
        try:
            for i in self.loop_over_fp(infile):
                file_out.write(i)
        finally:
            file_out.close()


class ArdisColor:
    """
    A Swiss-Army-Knife class for colors.
    :param input_color: needs to be either hex="hex color" or hsv_float="hsv tuple"
    """

    def __init__(self, **input_color):
        self.hex_chars = "0123456789ABCDEF"
        for k, v in input_color.items():
            self.color255 = self.convert(old=k, new="255", value=v)

    def convert(self, old=str, new=str, value=str):
        """
        :param old: str
        :param new: str
        :param value: str or tuple
        :rtype : tuple
        """
        if old == "hex":
            if value[0] == "#":
                value = value[1::]
            hex_tuple = (value[0:2], value[2:4], value[4:6])
            tuple_255 = map(self.to255, hex_tuple)
            if new == "255":
                return tuple_255
        if old == "hsv_float":
            assert isinstance(value, tuple)
            hsv_float_tuple = value
            rgb_float_tuple = colorsys.hsv_to_rgb(*hsv_float_tuple)
            tuple_255 = tuple(int(i * 255) for i in rgb_float_tuple)
            if new == "255":
                return tuple_255
        return None

    def to255(self, hex_str):
        """
        :type hex_str: str
        :rtype : int
        """
        total = 0
        for i in hex_str:
            new_total = total * 16
            total = new_total + self.hex_chars.index(i)
        return total

    def to_hex(self, str255):
        """

        :param str255: Can be any data type representing the value (out of 255). Will be converted to int for use.
        :rtype : str
        """
        int255 = int(str255)
        hexadec_slice = divmod(int255, 16)
        hexadec_tuple = tuple(self.hex_chars[i] for i in hexadec_slice)
        hex_str = "".join(hexadec_tuple)
        return hex_str

    @property
    def color_hex(self):
        """
        :rtype : tuple
        """
        hex_str_tuple = map(self.to_hex, self.color255)
        return hex_str_tuple

    @property
    def color_hex_str(self):
        """
        :rtype : str
        """
        return "#" + "".join(self.color_hex)

    @property
    def saturation(self):
        """
        :rtype : int
        """
        min_num = min(self.color255)
        max_num = max(self.color255)
        saturation = ((max_num - min_num) * 100) / 255
        return saturation

    @property
    def value(self):
        """
        :rtype : int
        """
        max_num = max(self.color255)
        value = (max_num * 100) / 255
        return value

    @property
    def rgb_float(self):
        """
Gives a tuple of floating point values representing the (r, g, b).
        :rtype : tuple
        """
        color_float = tuple((float(i) / 255) for i in self.color255)
        return color_float

    @property
    def hsv_float(self):
        """
Gives a tuple of floating point values representing the (h, s, v).
        :rtype : tuple
        """
        hsv_tuple = colorsys.rgb_to_hsv(*self.rgb_float)
        return hsv_tuple

    @property
    def hsv_normal(self):
        """
Gives a tuple of int values representing the (h, s, v) with the maxes (255, 100, 100).
        :rtype : tuple
        """
        hsv_tup = self.hsv_float
        tuple_255 = (int(hsv_tup[0] * 255), int(hsv_tup[1] * 100), int(hsv_tup[2] * 100))
        return tuple_255


if __name__ == "__main__":
    from os import environ as evar_dict

    if evar_dict.get('PYCHARM_HOSTED') == '1':
        # if __debug__ is True:
        test_color = ArdisColor(hex="#FF33AA")
        print test_color.color255
        print test_color.color_hex
        print test_color.color_hex_str
        print test_color.hsv_float
        print test_color.hsv_normal
        old_hsv = test_color.hsv_float
        new_hsv = ((old_hsv[0] - 0.5), old_hsv[1], old_hsv[2])
        test_color2 = ArdisColor(hsv_float=new_hsv)
        print test_color2.color_hex_str
        exit()

    (options, args) = parser.parse_args()

    filterer = LineProcessor()
    filterer.import_options(options)

    file_input = open(options.in_filename, 'r')
    file_output = open(options.out_filename, 'w')

    el_c = 0

    try:
        for line in file_input:
            if options.el_to_clean == "text":
                m_start = None
                m_start = re.search(r'^\s*<text|^\s*<tspan', line)
                if m_start:
                    el_c += 1
            if el_c == 0:
                filtered_line = line

                filtered_line = filterer.do_resize_filter(filtered_line)
                filtered_line = filterer.do_shadow_filter(filtered_line)
                filtered_line = filterer.do_colorize_filter(filtered_line)
                filtered_line = filterer.do_white_filter(filtered_line)

                file_output.write(filtered_line)
            else:
                m_end = None
                m_end = re.search(r'^\s*..text.|.*\s/>', line)
                if m_end:
                    el_c -= 1

    finally:
        file_input.close()
        file_output.close()

    if options.export_filename:
        e_fname_pattern = re.match('.*(\.(png|xpm))', options.export_filename)
        if e_fname_pattern:
            export_ext = str(e_fname_pattern.group(1))
            new_e_fname = re.sub('\.svg$', export_ext, options.out_filename)
        else:
            new_e_fname = options.export_filename
        import shlex
        import subprocess

        command_line = str('/usr/bin/convert -background "none" "' + options.out_filename + '" "' + new_e_fname + '"')
        clargs = shlex.split(command_line)
        subprocess.Popen(clargs)

    exit()