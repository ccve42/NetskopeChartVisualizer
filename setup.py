#!/usr/bin/env python3

import sys
from distutils.sysconfig import get_python_lib

from setuptools import setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write("""
==========================
Unsupported Python version
==========================

NS-GRAPH requires Python {}.{}, but you're trying to
install it on Python {}.{}.

""".format(*(REQUIRED_PYTHON + CURRENT_PYTHON)))
    sys.exit(1)

setup(
    entry_points = {'console_scripts': ['ns-graph = ns_graph:main']}
)
