# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

from common import strip_list

def IP2domain(IP_url_file,domain_and_ip_file):
    fp_url = open(IP_url_file,"r")
    result_url_list = fp_url.readlines() #notice the readlines,if use twice ,the second will no content ,the point will move to end
    result_url_list = strip_list(result_url_list)
    fp_url.close()
    source_url_list = result_url_list

    fp_domain_ip = open(domain_and_ip_file, "r")
    domain_ip_list = fp_domain_ip.readlines()
    domain_ip_list = strip_list(domain_ip_list)
    fp_domain_ip.close()

    for ipurl in source_url_list:
        ip = ipurl.split(":")[1].replace("//","")
        for item in domain_ip_list:
            if ip in item and len(item.split()) >=2:
                domain = item.split()[0]
                url = ipurl.replace(ip,domain)
                result_url_list.append(url)
                if ipurl in result_url_list: #maybe the ipurl has been removed before
                    result_url_list.remove(ipurl)

    result_url_list = list(set(result_url_list))
    fp = open(IP_url_file,"w")
    fp.writelines("\n".join(result_url_list))
    fp.close()

if __name__ == "__main__":
    a = "E:\wolaidai\github\Ashe\\task\douban\douban_urls_by_ashe.txt"
    b = "E:\wolaidai\github\Ashe\\task\douban\Teemo-douban.com-2017-11-05-10-38.txt"
    IP2domain(a,b)

'''
def IPorDomain(domain_ip_filename, IP_URL_list):
    result_list = IP_URL_list
    #print result_list
    domain_ip_list =  open(domain_ip_filename,"r").readlines()
    for IP_URL in IP_URL_list:
        IP = IP_URL.split("//")[1].split(":")[0]
        for domain_ip in domain_ip_list:
            domain_ip =  domain_ip.strip()
            if IP in domain_ip and len(domain_ip.split())>=2:
                domain = domain_ip.split()[0]
                newitem = IP_URL.replace(IP,domain)
                result_list.append(newitem)
                if IP_URL in IP_URL_list:
                    result_list.remove(IP_URL)
    return list(set(result_list))
'''



