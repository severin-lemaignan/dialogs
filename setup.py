 #!/usr/bin/env python
 # -*- coding: utf-8 -*-

import os
from distutils.core import setup

def readme():
    with open('README') as f:
        return f.read()

setup(name='Dialogs',
      version='0.9',
      license='BSD',
      description='Handles natural language inputs and outputs on cognitive robots',
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      author='OpenRobots team',
      author_email='openrobots@laas.fr',
      url='http://dialogs.openrobots.org',
      install_requires=['pyoro'],
      package_dir = {'': 'src'},
      packages=['dialogs', 'dialogs.interpretation', 'dialogs.parsing', 'dialogs.helpers', 'dialogs.verbalization'],
      scripts=['scripts/dialogs', 'scripts/dialogs_test'],
      data_files=[('share/dialogs', ['share/dialogs/' + f for f in os.listdir('share/dialogs')]),
                  ('share/doc/dialogs', ['AUTHORS', 'LICENSE', 'TODO', 'README']),
                  ('share/doc/dialogs', ['doc/' + f for f in os.listdir('doc/') if f != "demo"]),
                  ('share/examples/dialogs', ['share/examples/dialogs/' + f for f in os.listdir('share/examples/dialogs')])]
      )
