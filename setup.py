from distutils.core import setup


setup(name='ArdisBuilder',
      version='1.1',
      author='Ethan Randall',
      author_email='iJunkie22@gmail.com',
      url='https://github.com/iJunkie22/Ardis-Builder',
      packages=['ardisBuilder'],
      package_dir={'ardisBuilder': 'ardisBuilder'},
      package_data={'ardisBuilder': ['ui/ui.glade',
                                     'ui/icons/*.png',
                                     'ui/Images/*.svg',
                                     'ui/Images/*.png'
                                     ]
                    },
      scripts=['ardisBuilder/ardisutils.py']
      )