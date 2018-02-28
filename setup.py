#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# This file is mostly cribbed from Kenneth Reitz's example here:
# https://github.com/kennethreitz/twitter-scraper/blob/master/setup.py
#

import io
import os
import sys
from shutil import rmtree

from setuptools import Command, setup

NAME = "mt103"
DESCRIPTION = "Parse MT103 messages from the Swift payments network"
URL = "https://github.com/danielquinn/mt103"
EMAIL = "code@danielquinn.org"
AUTHOR = "Daniel Quinn"
VERSION = "0.0.1"

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = "\n" + f.read()


class UploadCommand(Command):
    """
    Support setup.py upload.
    """

    description = "Build and publish the package."
    user_options = []

    @staticmethod
    def status(s):
        """
        Prints things in bold.
        """
        print("\033[1m{0}\033[0m".format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status("Removing previous builds…")
            rmtree(os.path.join(here, "dist"))
        except OSError:
            pass

        self.status("Building Source and Wheel (universal) distribution…")
        os.system("{} setup.py sdist bdist_wheel --universal".format(
            sys.executable))

        self.status("Uploading the package to PyPi via Twine…")
        os.system("twine upload dist/*")

        sys.exit()


# Where the magic happens:
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    py_modules=["mt103"],
    include_package_data=True,
    license="GPL3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Office/Business :: Financial",
    ],
    cmdclass={
        "upload": UploadCommand,
    },
)
