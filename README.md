Ardis-Builder
=============

 ![Supported AL](https://img.shields.io/badge/Arch%20Linux-%3F-ff69b4.svg)
 ![Supported UL](https://img.shields.io/badge/Ubuntu%2FKubuntu-13.10%2C%2014.04%2C%2014.10-red.svg)
 ![Supported OS X](https://img.shields.io/badge/OS%20X-10.9%2C%2010.10-blue.svg)
 
 ![Supported Python](https://img.shields.io/badge/Python-2.7-brightgreen.svg)
 ![Supported GTK+](https://img.shields.io/badge/GTK%2B-3.4%2C%203.6%2C%203.8%2C%203.10%2C%203.12%2C%203.14%2C%203.16-orange.svg)

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
 
