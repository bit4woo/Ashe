# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import os.path
from lib.xmlparser import *
from WVS.WVS10 import *

def interactive():
    t = tabCompleter()
    print colors.white + "\n\nWelcome to interactive mode!\n\n" + colors.normal

    task_home_dir = os.path.join(os.path.dirname(__file__), "task")
    tasks = os.listdir(task_home_dir)
    print "{0} tasks existed:\n".format(len(tasks))
    for item in tasks:
        print item

    task_name = raw_input("Inout a existed task name to operate it or Input a new task name to create:")
    task_dir = os.path.join(task_home_dir,task_name)

    if os.path.isdir(task_dir):
        print "the task already exist, operate this task? (Y/n)"
        index = '''
        Please chose what to do:
        1. Please input the xml file
        2. Add URLs to WVS to scan
        4. Query high vuln from wvs
        '''
        choice = raw_input(index)
        index = '''
        1. Delete the task
        2. input a new task name 
        3. Query high vuln from wvs
        '''
        if choice == 1:
            target = raw_input("Please input the xml file")
            if os.path.isfile(target):
                urls = GetHttp()
        if choice == 2:
            target = raw_input("parse xml, please input the xml file")
    else:
        os.mkdir(task_dir)

        urls = os.path.join(task_dir, "urls.txt")
        urls_scanned = os.path.join(task_dir, "urls_scanned.txt")

        xmlfile = raw_input("Please input the xml file")
        if os.path.isfile(xmlfile):
            url_list = GetHttp(xmlfile)
            fp = open(urls, "w")
            fp.writelines("\n".join(url_list))
            fp.close()

        comfirm = raw_input("Add urls to scan?(Y/n)")
        if comfirm =="" or "Y" or "Yes":
            endindex = AddToWVS(urls)
            fp = open(urls,"rw")
            fp.



if __name__ == "__main__":
    print os.path.dirname(__file__)