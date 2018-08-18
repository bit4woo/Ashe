# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

#http://0cx.cc/about_awvs11_api.jspx
'''
targetURL = "https://127.0.0.1:3443/api/v1/targets"
scanning_profile = "https://127.0.0.1:3443/api/v1/scanning_profiles"
scanURL = "https://127.0.0.1:3443/api/v1/scans"
scanStatusURL = "https://127.0.0.1:3443/api/v1/scans"
scanStatusByID = "https://127.0.0.1:3443/api/v1/scans/56d847bc-344b-4513-a960-69e7d1988a46"
scanStop = "https://127.0.0.1:3443/api/v1/scans/56d847bc-344b-4513-a960-69e7d1988a46/abort"
https://localhost:3443/api/v1/targets/4696a02a-8b7e-441f-b039-4be476c66552

getReportTemplate = "https://127.0.0.1:3443/api/v1/report_templates"
genReport = "https://127.0.0.1:3443/api/v1/reports"
'''

import json
import requests
import requests.packages.urllib3
from lib.common import *

'''
import requests.packages.urllib3.util.ssl_
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = 'ALL'

or 

pip install requests[security]
'''
requests.packages.urllib3.disable_warnings()

tarurl = "https://127.0.0.1:3443"
apikey = "1986ad8c0a5b3df4d7028d5f3c06e936c606563d17c7046798a1f4569c961bc56"
headers = {"X-Auth": apikey, "content-type": "application/json"}


def addTask(url=''):
    # 添加任务
    data = {"address": url, "description": url, "criticality": "10"}
    try:
        response = requests.post(tarurl + "/api/v1/targets", data=json.dumps(data), headers=headers, timeout=30,
                                 verify=False)
        result = json.loads(response.content)
        return result['target_id']
    except Exception as e:
        print(str(e))
        return

def getTargetList():
    # 获取全部的扫描状态
    targets = []
    next_cursor=0
    while True:
        try:
            response = requests.get(tarurl + "/api/v1/targets?c="+str(next_cursor), headers=headers, timeout=30, verify=False)
            results = json.loads(response.content)
            tmp_next_cursor = results["pagination"]["next_cursor"]
            for result in results['targets']:
                targets.append(result['target_id'])
            if tmp_next_cursor !="null" and tmp_next_cursor!=None:
                next_cursor = int(tmp_next_cursor)
                continue
            return list(set(targets))
        except Exception as e:
            raise e

def getScanList():
    # 获取全部的扫描状态
    targets = []
    next_cursor =0
    while True:
        try:
            response = requests.get(tarurl + "/api/v1/scans?c="+str(next_cursor), headers=headers, timeout=30, verify=False)
            results = json.loads(response.content)

            #print results["pagination"]
            tmp_next_cursor = results["pagination"]["next_cursor"]
            #print tmp_next_cursor

            for result in results['scans']:
                targets.append(result['scan_id'])
                #print "scan list that already exist:"
                #print result['scan_id'], result['target']['address'], getScanStatus(result['scan_id'])  # ,result['target_id']
            if tmp_next_cursor !="null" and tmp_next_cursor!=None:
                next_cursor = tmp_next_cursor
                continue
            return list(set(targets))
        except Exception as e:
            raise e

def startScan(url):
    # 添加任务获取target_id
    # 开始扫描
    target_id = addTask(url)
    data = {"target_id": target_id, "profile_id": "11111111-1111-1111-1111-111111111111",
            "schedule": {"disable": False, "start_date": None, "time_sensitive": False}}
    try:
        response = requests.post(tarurl + "/api/v1/scans", data=json.dumps(data), headers=headers, timeout=30,
                                 verify=False)
        result = json.loads(response.content)
        print "{0} added successfully".format(url)
        return result['target_id']
    except Exception as e:
        print(str(e))
        return


def getScanStatus(scan_id):
    # 获取scan_id的扫描状况
    try:
        response = requests.get(tarurl + "/api/v1/scans/" + str(scan_id), headers=headers, timeout=30, verify=False)
        result = json.loads(response.content)
        status = result['current_session']['status']
        # 如果是completed 表示结束.可以生成报告
        if status == "completed":
            return getReport(scan_id)
        else:
            return result['current_session']['status']
    except Exception as e:
        print(str(e))
        return


def getReport(scan_id):
    # 获取scan_id的扫描报告
    data = {"template_id": "11111111-1111-1111-1111-111111111111",
            "source": {"list_type": "scans", "id_list": [scan_id]}}
    try:
        response = requests.post(tarurl + "/api/v1/reports", data=json.dumps(data), headers=headers, timeout=30,
                                 verify=False)
        result = response.headers
        report = result['Location'].replace('/api/v1/reports/', '/reports/download/')
        return tarurl.rstrip('/') + report
    except Exception as e:
        print(str(e))
        return

def AddScans(url_list):
    targets = strip_list(getScanList())
    url_list = strip_list(url_list)

    for url in url_list:
        if url in targets:
            print "{0} already in scan list,skip".format(url)
        else:
            id = startScan(url)
            getReport(id)

    return url_list.index(url)+1

def delTargets(target_id_list):
    "https://localhost:3443/api/v1/targets/4696a02a-8b7e-441f-b039-4be476c66552"
    proxy ={"http":"http://127.0.0.1:8080","https":"https://127.0.0.1:8080"}
    for target_id in target_id_list:
        url =  tarurl + "/api/v1/targets/" + str(target_id)
        response = requests.delete(tarurl + "/api/v1/targets/" + str(target_id), headers=headers, timeout=30, verify=False,proxies =proxy)
        #print response.content

def delScans(Scan_id_list):
    for scan_id in Scan_id_list:
        response = requests.delete(tarurl + "/api/v1/scans/" + str(scan_id), headers=headers, timeout=30, verify=False)
        #print response.content

if __name__ == '__main__':
    urls = ["http://www.baidu.com",'http://testhtml5.vulnweb.com/']
    print AddScans(urls)
    #delScans(getScanList())
    #delTargets(getTargetList())