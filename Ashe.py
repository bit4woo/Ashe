# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import os.path
import shutil

from lib.WVS10 import *
from lib.color import color
from lib.xmlparser import *


def interactive():
    #t = tabCompleter()
    print color.G+"\n\nWelcome to interactive mode!\n\n"

    task_home_dir = os.path.join(os.path.dirname(__file__), "task")
    while True:
        # print already existed task
        tasks = os.listdir(task_home_dir)
        for task in tasks:
            if os.path.isfile(task):
                tasks.remove(task)
        print "{0}[{1}]{2} tasks existed:".format(color.R,len(tasks),color.G)
        for item in tasks:
            print item

        print(color.Y+"\n\n"
              "*.Input a existed task name to operate it or Input a new task name to create.\n"
              "*.Input q to query vuln from wvs.\n"
              "*.Input x to exit Ashe.\n"
              "\n"+color.W)
        task_name = raw_input("==>")
        if task_name.lower() == "q":
            QueryFromWVS()
        elif task_name.lower() in ['x','back']:
            break
        elif task_name == "":
            continue
        else:
            task_dir = os.path.join(task_home_dir,task_name)

            if os.path.isdir(task_dir):
                choice = raw_input("the task already exist, operate this task? (Y/n)")
                if choice.lower() not in ["y","yes",""]:
                    continue
            else:
                os.mkdir(task_dir)
                print "task {0} created, chose what to do:".format(task_name)

            urls_file = os.path.join(task_dir, "{0}_urls_by_ashe.txt".format(task_name))
            urls_scanned_file = os.path.join(task_dir, "{0}_urls_scanned_by_ashe.txt".format(task_name))
            while True:
                index = '''
                [Current Task: {0}]
                1. Delete this task
                2. Input the xml file and parse to urls
                3. Add urls to scan
                4. back
                ==>
                '''.format(task_name)
                choice = raw_input(index)
                if choice == "1":
                    delete = raw_input("Are you sure to DELETE this task?(y/N)")
                    if delete.lower() in ["y","yes"]:
                        shutil.rmtree(task_dir)
                        break
                    else:
                        continue
                elif choice == "2":
                    xmlfile = raw_input("parse xml, please input the xml file:==>")
                    xmlfile = xmlfile.strip()
                    if os.path.isfile(xmlfile):
                        des_xml_file = os.path.join(task_dir, os.path.basename(xmlfile))
                        if os.path.abspath(xmlfile) == os.path.abspath(des_xml_file):# same file
                            pass
                        elif os.path.exists(des_xml_file):
                            copy_choice = raw_input("The file already exist,Overwirte or keep Two(O/t)?")
                            if copy_choice.lower() in ["","o"]:
                                shutil.copyfile(xmlfile, des_xml_file) # overwrite
                            elif copy_choice.lower() == "t":
                                des_xml_file = os.path.join(task_dir, os.path.basename(xmlfile).split(".")[0]+"_1"+os.path.basename(xmlfile).split(".")[1])
                                shutil.copy(xmlfile, des_xml_file)
                            else:
                                continue
                        else:
                            shutil.copy(xmlfile, des_xml_file)
                        url_list = GetHttp(xmlfile)
                        fp = open(urls_file, "w")
                        fp.writelines("\n".join(url_list))
                        fp.close()
                    else:
                        print "File do not exist!"
                        continue
                elif choice == "3":
                    if os.path.isfile(urls_file):
                        fp = open(urls_file,"r")
                        urls = fp.readlines()
                        fp.close()
                        end_index = AddToWVS(urls)
                        print "{0} urls added".format(end_index+1)
                        if end_index >= 0:
                            urls_left = urls[end_index+1:-1]
                            urls_scanned = urls[0:end_index]
                        fp = open(urls_file,"w")
                        fp.writelines(urls_left)
                        fp.close()

                        fp = open(urls_scanned_file,"a")
                        fp.writelines(urls_scanned)
                        fp.write("____above urls added to scan at {0}______\n".format(datetime.datetime.now().strftime("%m/%d/%Y %H%M")))
                        fp.close()
                        break
                    else:
                        print "{0} not found!".format(urls_file)
                elif choice.lower() in ["4",'back','exit']:
                    break
                else:
                    continue

if __name__ == "__main__":
    interactive()