#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
origin:
http://xmpppy.sourceforge.net/examples/bot.py
'''

from init_env import USERNAME, PASSWORD, SERVER, PORT
from init_env import WHITE_LIST_USERS

import pdb
import sys
import xmpp

from get_ip import get_ip

commands = {}
i18n = {
    'zh_CN': {},
    'en': {}
    }
########################### user handlers start ##################################
i18n['en']['HELP'] = "This is example jabber bot.\nAvailable commands: %s"

def helpHandler(user, command, args, msg):
    lst = commands.keys()
    lst.sort()
    return "HELP", ',  '.join(lst)
commands['help'] = helpHandler

i18n['en']['EMPTY'] = "%s"
i18n['en']['HOOK1'] = 'Responce 1: %s'
def hook1Handler(user, command, args, msg):
    return "HOOK1", 'You requested: %s'%args
commands['hook1'] = hook1Handler

i18n['en']['HOOK2'] = 'Responce 2: %s'
def hook2Handler(user, command, args, msg):
    return "HOOK2", "hook2 called with %s"%(`(user, command, args, msg)`)
commands['hook2'] = hook2Handler

i18n['en']['HOOK3'] = 'Responce 3: static string'
def hook3Handler(user, command, args, msg):
    return "HOOK3"*int(args)
commands['hook3'] = hook3Handler

def get_ip_hook(user, command, args, msg):
    # print '>>> get_ip_hook'
    # print 'user:', user
    # print 'command:', command
    # print 'args:', args
    # print 'msg:', msg
    for i in WHITE_LIST_USERS:
        if str(user).find(i) != -1:
            return str(get_ip()).strip()
        
commands['ip'] = get_ip_hook
########################### user handlers stop ###################################

############################ bot logic start #####################################
i18n['en']["UNKNOWN COMMAND"] = 'Unknown command "%s". Try "help"'
i18n['en']["UNKNOWN USER"] = "I do not know you. Register first."

def message_callback(conn, msg):
    text = msg.getBody()
    user = msg.getFrom()
    user.lang = 'en'      # dup
    if text.find(' ')+1: command, args = text.split(' ', 1)
    else: command, args = text, ''
    cmd = command.lower()

    if commands.has_key(cmd): reply = commands[cmd](user, command, args, msg)
    else: reply = ("UNKNOWN COMMAND", cmd)

    if type(reply) == type(()):
        key, args = reply
        if i18n[user.lang].has_key(key): pat = i18n[user.lang][key]
        elif i18n['en'].has_key(key): pat = i18n['en'][key]
        else: pat = "%s"
        if type(pat) == type(''): reply = pat%args
        else: reply = pat(**args)
    else:
        try: reply = i18n[user.lang][reply]
        except KeyError:
            try: reply = i18n['en'][reply]
            except KeyError: pass
    if reply: conn.send(xmpp.Message(msg.getFrom(), reply))

############################# bot logic stop #####################################

def StepOn(conn):
    try:
        conn.Process(1)
    except KeyboardInterrupt:
        return False
    return True

def GoOn(conn):
    while StepOn(conn):
        pass

def main():        
    if USERNAME == '' or PASSWORD == '' or SERVER == '':        
        print "Usage: bot.py username@server.net password"
        sys.exit(0)
        
    # jid = xmpp.JID(USERNAME)
    # user, server, password = jid.getNode(), jid.getDomain(), PASSWORD

    # conn = xmpp.Client(server)#, debug = [])
    conn = xmpp.Client('gmail.com', debug = [])
    # conres = conn.connect()
    conres = conn.connect(server=(SERVER, PORT))
    if not conres:
        print "Unable to connect to server %s!" % SERVER
        sys.exit(1)

    if conres not in ('tls', 'ssl'):
        print "Warning: unable to estabilish secure connection - both TLS and SSL failed!"
    else:
        print 'Using secure connection - %s' % conres
        
    # authres = conn.auth(user, password)
    authres = conn.auth(USERNAME, PASSWORD)    
    if not authres:
        print "Unable to authorize on %s - check login/password." % SERVER
        sys.exit(1)
        
    if authres != 'sasl':
        print "Warning: unable to perform SASL auth os %s. Old authentication method used!" % SERVER
        
    conn.RegisterHandler('message', message_callback)
    conn.sendInitPresence()
    print "Bot started."
    
    GoOn(conn)

if __name__ == '__main__':
    main()
