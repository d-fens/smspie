#!/usr/bin/env python
from distutils.core import setup
from setuptools import find_packages
 
setup(name='py-smspie',
      version='0.1',
      description='Python application for sending SMS via the providers web interface',
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
