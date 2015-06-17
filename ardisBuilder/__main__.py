#!/usr/bin/python2.7
__author__ = 'Ethan Randall'

import ardisBuilder.ardisbuilderapp

try:
    ardisBuilder.ardisbuilderapp.ArdisBuilder.make_desktop_launcher()

except IOError:
    pass

ardisBuilder.ardisbuilderapp.start()
