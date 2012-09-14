#!/usr/bin/python
# -*- coding: utf-8 -*-
# (c) 2012 Niko Böckerman <niko.bockerman@gmail.com>
# Released under the terms of the 2-clause BSD license.

from distutils.core import setup

import os.path, sys

setup(
    name = 'rsnapshot-backup',
    version = '1.0a1',
    author = 'Niko Böckerman',
    author_email = 'niko.bockerman@gmail.com',
    url = 'https://github.com/nikobockerman/rsnapshot-backup',

    packages = ['rsnapshotbackup'],
    scripts = ['bin/rsnapshot-backup'],

    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: System :: Archiving :: Backup'
    ]
)
