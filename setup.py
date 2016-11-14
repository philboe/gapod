#!/usr/bin/env python3.5

import distutils.core

name = 'gapod.py'

distutils.core.setup(name=name,
        version='1.0',
        author="Philipp Bösch",
        author_email="boeschphil@gmail.com",
        url="https://github.com/philboe/gapod",
        description="Sets current wallpaper to Astronomy picture of the day", 
        py_modules=['gapod/gapod.py'])
