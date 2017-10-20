# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import readline,glob
import datetime

def strip_list(inputlist):
    if isinstance(inputlist,list):
        resultlist =[]
        for x in inputlist:
            x = x.strip()
            resultlist.append(x)
        return resultlist
    else:
        print "the input should be a list"

class colors:
    white = "\033[1;37m"
    normal = "\033[0;00m"
    red = "\033[1;31m"
    blue = "\033[1;34m"
    green = "\033[1;32m"
    lightblue = "\033[0;34m"

class tabCompleter():
    def __init__(self,CMD_pool):
        self.cmd = CMD_pool

    def pathCompleter(self,text,state):
        line   = readline.get_line_buffer().split()
        return [x for x in glob.glob(text+'*')][state]

    def WVS_query_completer(self,text, state):
        options = [cmd for cmd in self.cmd if cmd.startswith(text)]
        if state < len(options):
            return options[state]
        else:
            return None

    readline.parse_and_bind("tab: complete")
    readline.set_completer(WVS_query_completer)

def nowstr():
    now = datetime.datetime.now() + datetime.timedelta(minutes=+3)
    now = datetime.datetime.now()
    datestr = now.strftime("%m/%d/%Y")