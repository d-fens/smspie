#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup
 
setup(name='smspie',
      version='0.2',
      description='Send SMS messages using the providers website.',
      author='d-fens',
      url='http://github.com/d-fens/smspie/',
      license = 'MIT',
      packages=['smspie', 'smspie/providers/'],
      scripts=['scripts/smspie'],
      install_requires=[
            'PyYAML', 'BeautifulSoup', 'pycurl'
      ],
      classifiers=[
            'Environment :: Console',
            'Natural Language :: English',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
            'Programming Language :: Python'
      ])
