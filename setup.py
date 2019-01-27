#!/usr/bin/env python3
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: InfinityFuture
# Mail: infinityfuture@foxmail.com
# Created Time: 2019-01-27 10:00:00
#############################################

import os
from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    'requests'
]

VERSION = os.path.join(
    os.path.realpath(os.path.dirname(__file__)),
    'version.txt'
)

setup(
    name='infnlp',
    version=open(VERSION, 'r').read().strip(),
    keywords=('pip', 'NLP', 'HanLP'),
    description='NLP tool',
    long_description='NLP tool',
    license='Private',
    url='https://github.com/infinity-future/InfNLP',
    author='infinityfuture',
    author_email='infinityfuture@foxmail.com',
    packages=find_packages(exclude=['*hanlp_backend*']),
    include_package_data=True,
    platforms='any',
    install_requires=INSTALL_REQUIRES
)
