 #!/usr/bin/env python
 # -*- coding: utf-8 -*-

import os
from distutils.core import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='Dialogs',
      version='0.14',
      license='BSD',
      description='Handles natural language inputs and outputs on cognitive robots',
      long_description=readme(),
      classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Text Processing :: Linguistic',
      ],
      author='Séverin Lemaignan',
      author_email='severin.lemaignan@epfl.ch',
      url='http://dialogs.openrobots.org',
      requires=['pykb'],
      package_dir = {'': 'src'},
      packages=['dialogs', 'dialogs.interpretation', 'dialogs.parsing', 'dialogs.helpers', 'dialogs.verbalization'],
      scripts=['scripts/dialogs', 'scripts/dialogs_test'],
      data_files=[('share/dialogs', ['share/dialogs/' + f for f in os.listdir('share/dialogs')]),
                  ('share/doc/dialogs', ['AUTHORS', 'LICENSE', 'TODO', 'README.md']),
                  ('share/doc/dialogs', ['doc/' + f for f in os.listdir('doc/') if f != "demo"]),
                  ('share/examples/dialogs', ['share/examples/dialogs/' + f for f in os.listdir('share/examples/dialogs')])]
      )
