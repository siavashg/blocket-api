#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
 
setup(
    name='blocket-python-sdk',
    version='0.01',
    description='This client library is designed to support the Blocket REST API',
    author='Siavash Ghorbani',
    url='http://github.com/siavashg/blocket-api',
    package_dir={'': 'src'},
    py_modules=[
        'blocket',
    ],
)
