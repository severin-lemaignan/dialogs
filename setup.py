 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import os
from distutils.core import setup

setup(name='Dialog',
      version='0.2.99',
      license='BSD',
      description='Handles natural language inputs and outputs on cognitive robots',
      long_description='Dialog parses natural language and tries to ground it with respect to an ontology that is maintained by the robot',
      author='OpenRobots team',
      author_email='openrobots@laas.fr',
      url='http://softs.laas.fr/openrobots',
      package_dir = {'': 'src'},
      packages=['dialog', 'dialog.interpretation', 'dialog.parsing', 'dialog.verbalization'],
      scripts=['scripts/dialog', 'scripts/dialog_test'],
      data_files=[('share/dialog', ['share/dialog/' + f for f in os.listdir('share/dialog')]),
                  ('share/doc/dialog', ['AUTHORS', 'LICENSE', 'TODO', 'README']),
                  ('share/doc/dialog', ['doc/' + f for f in os.listdir('doc')]),
                  ('share/examples/dialog', ['share/examples/dialog/' + f for f in os.listdir('share/examples/dialog')])]
      )
