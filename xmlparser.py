#!/usr/bin/env python
# -*- encoding:utf-8 -*-

# Lee Li <shuge.lee@gmail.com>

from pprint import pprint as pp
from xml.dom.minidom import parseString

msg = '''<message xmlns="jabber:client" to="flyinflash@gmail.com" type="chat" id="ffe3fad9-0796-4ec0-b98c-cbbb23485871" from="shuge.lee@gmail.com/013dff98"> <body>ip</body>
<x xmlns="google:nosave" value="disabled" /><record xmlns="http://jabber.org/protocol/archive" otr="false" /></message>'''

def main():
    msg_dom_element = parseString(msg).childNodes[0]
    msg_from = msg_dom_element.attributes['from'].value
    msg_body = msg_dom_element.getElementsByTagName('body')[0].childNodes[0].nodeValue
    
    print msg_from, msg_body
    
    return 0

if __name__ == '__main__':
    main()
    
