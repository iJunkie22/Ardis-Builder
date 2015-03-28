#!/usr/bin/python2.7
__author__ = 'Ethan Randall'

from . import ardisbuilderapp

try:
    ardisbuilderapp.ArdisBuilder.make_desktop_launcher()

except IOError:
    pass

ardisbuilderapp.start()