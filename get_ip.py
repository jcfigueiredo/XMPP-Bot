#!/usr/bin/env python
#coding:utf-8

from urllib import urlopen
import re
import socket
# from pprint import pprint as pp

URL='http://www.123cha.com/'
IP_PATTERN = r'([\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3})'

def get_ip():
    webpage_lines = urlopen(URL).read()
    webpage = ''.join(webpage_lines)
    #pp(webpage)

    # save_file = file('get_ip.txt', 'w')
    # save_file.writelines(webpage)
    # save_file.close()

    # prog= re.compile(IP_PATTERN)
    return re.findall(re.compile(IP_PATTERN), webpage)[0]

if __name__ == '__main__':
    print get_ip()

