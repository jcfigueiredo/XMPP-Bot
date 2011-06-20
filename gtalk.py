#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
Usage: gtalk.py foo@gmail.com "Message"

Requirement
    xmpppy/python-xmpp - Python library for communication with XMPP (Jabber) servers
'''

from init_env import USERNAME, PASSWORD, SERVER
import xmpp
import sys

HELP = 'Usage: gtalk.py foo@gmail.com "Message"'


def main():
    if len(sys.argv) < 3:
        print HELP
        sys.exit(0)

    client = 'underworld'
    port = 5222
    cnx = xmpp.Client(client or 'gmail.com', debug=[])
    # cnx = xmpp.Client('gmail.com')
    conres = cnx.connect(server=(SERVER, port or 5223))
    # print 'conres:', conres
    # cnx.auth(USERNAME, PASSWORD, 'python')
    cnx.auth(USERNAME, PASSWORD)        

    send_to = sys.argv[1]
    msg_text = sys.argv[2]

    cnx.send(xmpp.Message(send_to, msg_text))

if __name__ == '__main__':
    main()
