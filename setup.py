#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages
 
setup(name='smspie',
      version='0.2',
      description='Send SMS messages using the providers website.',
      author='d-fens',
      url='http://github.com/d-fens/smspie/',
      license = 'MIT',
      packages=['smspie', 'smspie/providers/'],
      scripts=['scripts/smspie'],
      classifiers=[
            'Environment :: Console',
            'Natural Language :: English',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python'
      ])
