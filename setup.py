 #!/usr/bin/python
 # -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='Dialog',
      version='0.1',
      description='Handles natural language inputs and outputs for the LAAS robots',
      author='OpenRobots team',
      author_email='openrobots@laas.fr',
      url='http://softs.laas.fr/openrobots',
      package_dir = {'': 'src'},
      packages=['dialog', 'dialog.interpretation', 'dialog.parsing', 'dialog.verbalization']
      )
