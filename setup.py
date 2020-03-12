#!/usr/bin/env python

from setuptools import setup, find_packages

about = {}
with open("hwut_server/__about__.py") as fp:
    exec(fp.read(), about)

setup(
    name=about['__title__'],
    version=about['__version__'],
    description=about['__summary__'],
    author=about['__author__'],
    author_email=about['__email__'],
    url=about['__uri__'],
    packages=find_packages(),
    install_requires=[
        'Flask >= 0.10.1',
        'Flask_SQLAlchemy >= 2.1',
        'SQLAlchemy >= 1.0.11',
        'Werkzeug >= 0.11.3',
        'passlib',
        #'psycopg2',
        'requests',
        'flask_script',
        'pyserial',
    ],
)
