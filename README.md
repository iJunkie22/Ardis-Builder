Ardis-Builder
=============

Official setup and customization wizard for the Ardis Icon Theme
####Artwork by Kotusworks	|	Code by iJunkie22
[GitHub](https://github.com/iJunkie22/Ardis-Builder) | [deviantART](http://kotusworks.deviantart.com/art/Ardis-Icon-Theme-450178304) | [Trello](https://trello.com/b/Rkn5p8kQ/ardis)



#Linux Requirements
*These packages will also automatically install the rest of what you need in order to run ArdisBuilder, if you obey their dependencies*

* `python-gi`
* `gir1.2-gladeui-2.0`


In case you are compiling from source instead of dpkg, here is a verbose list of dependencies:

* `GTK+` *(`3.4 or newer`)*
*  `python` *(`2.7x`)*
*  `python-gi`
*  `gir1.2-gladeui-2.0`
*  `gir1.2-gtk-3.0` 


#OSX Requirements (MacPorts Ports)
* librsvg
* py27-gobject3

>To install MacPorts, refer [here](https://www.macports.org/install.php)



####Installation:
Run `[YOUR_PYTHON] ./setup.py install` in the repo\'s root folder.

####Running:
`[YOUR_PYTHON] -m ardisBuilder`

And to use ardisutils:
`[YOUR_PYTHON] -m ardisBuilder.ardisutils [ARGUMENTS]`
 
