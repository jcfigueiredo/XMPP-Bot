#!/usr/bin/env python

from os import path as osp
PWD = osp.dirname(osp.realpath(__file__))
TMP_PATH = PWD
LOG_PATH = osp.join(TMP_PATH, 'bot.log')
PID_PATH = osp.join(TMP_PATH, 'bot.pid')

USERNAME = 'you@gmail.com'
PASSWORD   = 'secret'
SERVER = 'talk.google.com'

WHITE_LIST_USERS = ('somebody-you-like@gmail.com', )

if USERNAME.find('@') != -1:
    USERNAME = USERNAME[:USERNAME.find('@')]
