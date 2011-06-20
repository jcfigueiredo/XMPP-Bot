#!/usr/bin/env python

from os import path as osp
PWD = osp.dirname(osp.realpath(__file__))
TMP_PATH = PWD
LOG_PATH = osp.join(TMP_PATH, 'bot.log')
PID_PATH = osp.join(TMP_PATH, 'bot.pid')

#USERNAME = 'you@gmail.com'
#PASSWORD   = 'secret'
#SERVER = 'talk.google.com'

USERNAME = 'be01@underworld'
PASSWORD   = 'be01'
SERVER = 'underworld'


WHITE_LIST_USERS = (
    'be01@underworld',
    'be02@underworld',
    'be03@underworld',
    'be04@underworld',
    'fe01@underworld',
    'fe02@underworld',
    'fe03@underworld',
    'fe04@underworld',
    )


if USERNAME.find('@') != -1:
    USERNAME = USERNAME[:USERNAME.find('@')]
