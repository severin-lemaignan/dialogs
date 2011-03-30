 #!/usr/bin/env python
 # -*- coding: utf-8 -*-

import os
from distutils.core import setup

setup(name='Dialogs',
      version='0.5',
      license='BSD',
      description='Handles natural language inputs and outputs on cognitive robots',
      long_description='Dialogs parses natural language and tries to ground it with respect to an ontology maintained by the robot',
      author='OpenRobots team',
      author_email='openrobots@laas.fr',
      url='http://dialogs.openrobots.org',
      package_dir = {'': 'src'},
      packages=['dialogs', 'dialogs.interpretation', 'dialogs.parsing', 'dialogs.helpers', 'dialogs.verbalization'],
      scripts=['scripts/dialogs', 'scripts/dialogs_test'],
      data_files=[('share/dialogs', ['share/dialogs/' + f for f in os.listdir('share/dialogs')]),
                  ('share/doc/dialogs', ['AUTHORS', 'LICENSE', 'TODO', 'README']),
                  ('share/doc/dialogs', ['doc/' + f for f in os.listdir('doc')]),
                  ('share/examples/dialogs', ['share/examples/dialogs/' + f for f in os.listdir('share/examples/dialogs')])]
      )
