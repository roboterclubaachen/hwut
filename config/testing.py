# -*- coding: utf-8 -*-

TESTING = True

DEBUG = True
SQLALCHEMY_ECHO = True

ADMINS = frozenset(['raphael+hwut@rleh.de'])

SQLALCHEMY_DATABASE_URI = 'postgres://hwut_testing:hwut_testing@localhost/hwut_testing'
DATABASE_CONNECT_OPTIONS = {}

SQLALCHEMY_TRACK_MODIFICATIONS = True
