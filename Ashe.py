# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import os.path
import shutil

from lib.WVS10 import *
from lib.color import color
from lib.xmlparser import *
from lib.URLhelper import *
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.contrib.completers import PathCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory


taskDealIndex = '''
[Current Task: {0}]
1. Delete this task
2. Input the xml file and parse to urls
3. Input Teemo result file to replace IP to domain 
4. Add urls to scan
5. back
Task({0}):==>'''

def interactive():
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
        task_completer = WordCompleter(tasks, ignore_case=True)
        task_name = prompt(u"==>",completer=task_completer)
        if task_name.lower() == "q":
            QueryFromWVS()
        elif task_name.lower() in ['x','back']:
            break
        elif task_name == "":
            continue
        else:
            task_dir = os.path.join(task_home_dir,task_name)

            if os.path.isdir(task_dir):
                choice = prompt(u"the task already exist, operate this task? (Y/n)",)
                if choice.lower() not in ["y","yes",""]:
                    continue
            else:
                os.mkdir(task_dir)
                print "task {0} created, chose what to do:".format(task_name)

            urls_file = os.path.join(task_dir, "{0}_urls_by_ashe.txt".format(task_name))
            urls_scanned_file = os.path.join(task_dir, "{0}_urls_scanned_by_ashe.txt".format(task_name))
            while True:
                index = taskDealIndex.format(task_name)
                choice = prompt(unicode(index))
                if choice == "1":
                    delete = prompt(u"Are you sure to DELETE this task?(y/N)")
                    if delete.lower() in ["y","yes"]:
                        shutil.rmtree(task_dir)
                        break
                    else:
                        continue
                elif choice == "2":
                    path_completer = PathCompleter()
                    xmlfile = prompt(u"parse xml, please input the xml file==>",completer = path_completer,history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),)
                    xmlfile = xmlfile.strip()
                    if os.path.isfile(xmlfile):
                        des_xml_file = os.path.join(task_dir, os.path.basename(xmlfile))
                        if os.path.abspath(xmlfile) == os.path.abspath(des_xml_file):# same file
                            pass
                        elif os.path.exists(des_xml_file):
                            copy_choice = prompt(u"The file already exist,Overwirte or keep Two(O/t)?")
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
                        print(url_list)
                        if copy_choice.lower() in ["", "o"]:
                            fp = open(urls_file, "a") #overwrite
                        else:
                            fp = open(urls_file, "a+")  # add model,may mutipul result in a task
                        if len(fp.readlines()) ==0:
                            pass
                        else:
                            fp.write("\n")
                        fp.writelines("\n".join(url_list))
                        fp.close()
                    else:
                        print "File do not exist!"
                        continue
                elif choice == "3":
                    IP_domain_file = prompt(u"Input the file that contains domain and IP relationship(Teemo Result File)\n==>")
                    IP_domain_file = IP_domain_file.strip()
                    if os.path.isfile(IP_domain_file):
                        des_IP_Domain_file = os.path.join(task_dir, "Teemo-"+os.path.basename(IP_domain_file))
                        if os.path.abspath(IP_domain_file) == os.path.abspath(des_IP_Domain_file):# same file
                            pass
                        elif os.path.exists(des_IP_Domain_file):
                            shutil.copyfile(IP_domain_file, des_IP_Domain_file) # overwrite
                        else:
                            shutil.copy(IP_domain_file, des_IP_Domain_file)
                        IP2domain(urls_file,des_IP_Domain_file)
                    else:
                        print "File do not exist!"
                        continue

                elif choice == "4":
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
                elif choice.lower() in ["5",'back','exit']:
                    break
                else:
                    continue

if __name__ == "__main__":
    interactive()