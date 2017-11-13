# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from xml.dom.minidom import parse
import xml.dom.minidom
import sys


def GetHttp(xmlfilename):
    result_list = []
    DOMTree = xml.dom.minidom.parse(xmlfilename)
    collection = DOMTree.documentElement

    hosts = collection.getElementsByTagName("host")
    #print hosts
    for host in hosts:
        status = host.getElementsByTagName("status")[0]
        state = status.getAttribute("state")
        if state == "up": # host is up
            address = host.getElementsByTagName("address")[0]
            addr = address.getAttribute("addr")

            ports = host.getElementsByTagName('port')
            for port in ports:
                portid = port.getAttribute("portid")
                port_state = port.getElementsByTagName('state')[0]
                port_state = port_state.getAttribute("state")
                if port_state == "open": #port is open
                    try:
                        service = port.getElementsByTagName("service")[0]
                        name = service.getAttribute("name")
                        if "http" == name:
                            try:#<service name="http" product="nginx" tunnel="ssl" method="probed" conf="10">
                                tunnel=service.getAttribute("tunnel")
                                if tunnel == "ssl":
                                    IP_URL = "{0}://{1}:{2}".format("https", addr, portid)
                                    result_list.append(IP_URL)
                            except:
                                IP_URL =  "{0}://{1}:{2}".format(name,addr,portid)
                                result_list.append(IP_URL)
                        elif "https" == name:
                            IP_URL =  "{0}://{1}:{2}".format(name,addr,portid)
                            result_list.append(IP_URL)
                        elif "http" in name: #http-proxy、http-alt
                            IP_URL =  "{0}://{1}:{2}".format("http",addr,portid)
                            result_list.append(IP_URL)
                            IP_URL =  "{0}://{1}:{2}".format("https",addr,portid)
                            result_list.append(IP_URL)
                        elif name == "unknow":
                            try:
                                tunnel=service.getAttribute("tunnel")
                                if tunnel == "ssl":
                                    IP_URL = "{0}://{1}:{2}".format("https", addr, portid)
                                    result_list.append(IP_URL)
                            except:
                                pass
                    except Exception as e:
                        pass
    return list(set(result_list))


def GetService(xmlfilename):
    global loading
    global services
    supported = ['ssh','ftp','postgresql','telnet','mysql','ms-sql-s','rsh','vnc','imap','imaps','nntp','pcanywheredata','pop3','pop3s','exec','login','microsoft-ds','smtp','smtps','submission','svn','iss-realsecure']
    doc = xml.dom.minidom.parse(xmlfilename)
    for host in doc.getElementsByTagName("host"):
        try:
            address = host.getElementsByTagName("address")[0]
            ip = address.getAttribute("addr")
            eip = ip.encode("utf8")
            iplist = eip.split(',')
        except:
            # move to the next host
            continue
        try:
            status = host.getElementsByTagName("status")[0]
            state = status.getAttribute("state")
        except:
            state = ""
        try:
            ports = host.getElementsByTagName("ports")[0]
            ports = ports.getElementsByTagName("port")
        except:
            continue

        for port in ports:
            pn = port.getAttribute("portid")
            state_el = port.getElementsByTagName("state")[0]
            state = state_el.getAttribute("state")
            if state == "open":
                try:
                    service = port.getElementsByTagName("service")[0]
                    port_name = service.getAttribute("name")
                except:
                    service = ""
                    port_name = ""
                    product_descr = ""
                    product_ver = ""
                    product_extra = ""
                name = port_name.encode("utf-8")
                tmp_port = pn.encode("utf-8")
                if name in supported:
                    if name == "postgresql":
                        name = "postgres"
                    if name =="ms-sql-s":
                        name = "mssql"
                    if name == "microsoft-ds":
                        name = "smbnt"
                    if name == "pcanywheredata":
                        name = "pcanywhere"
                    if name == "shell":
                        name = "rsh"
                    if name == "exec":
                        name = "rexec"
                    if name == "login":
                        name = "rlogin"
                    if name == "smtps" or name == "submission":
                        name = "smtp"
                    if name == "imaps":
                        name = "imap"
                    if name == "pop3s":
                        name = "pop3"
                    if name == "iss-realsecure":
                        name = "vmauthd"
                    if name in services:
                        if tmp_port in services[name]:
                            services[name][tmp_port] += iplist
                        else:
                         services[name][tmp_port] = iplist
                    else:
                        services[name] = {tmp_port:iplist}
    loading = True



if __name__ == "__main__":

    if len(sys.argv) == 3:
        nmap_xml = sys.argv[1]
        teemo_domain_IP = sys.argv[2]

