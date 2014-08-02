#!/usr/bin/python
from gi.repository import Gtk
from gi.repository import GdkPixbuf
#import gdk-pixbuf
import os

w_path = os.getcwd()
pbuf = GdkPixbuf.Pixbuf()
#class Ardis_Pixbufs:

buffer_dict = {}

def cache_item(img_name):
  pixbuf_name = pbuf.new_from_file('Images/'+img_name)
  return img_name, pixbuf_name
  
pbuf.new_from_file('Images/'+img_name)
  
  
  
#pixbuf_dict = {}
  
#page_indicator1 = GdkPixbuf.Pixbuf.new_from_file('Images/page_indicator1.png')
#page_indicator2 = GdkPixbuf.Pixbuf.new_from_file('Images/page_indicator2.png')
blah1, blah2 = cache_item('page_indicator1.png')
print blah1, blah2
print blah2.get_width()
exit()