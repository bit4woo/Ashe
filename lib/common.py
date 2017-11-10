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

class tabCompleter():
    def __init__(self,CMD_pool):
        self.cmd = CMD_pool

    def pathCompleter(self,text,state):
        line   = readline.get_line_buffer().split()
        return [x for x in glob.glob(text+'*')][state]

    def WVS_query_completer(self,text, state):
        options = [cmd for cmd in self.cmd if text in cmd.lower()]
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

if __name__ == "__main__":
    li = ['aa___aaaaaa','b___bbbbbbbb','ccc___cccccc']
    readline.parse_and_bind("tab: complete")
    readline.set_completer(tabCompleter(li).WVS_query_completer)
    x = raw_input("==>")
