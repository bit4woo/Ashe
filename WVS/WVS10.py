# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'

import csv
import pyodbc
from lib.common import *
import datetime
import requests

possible_vuln = '''
.htaccess file readable
Apache httpd remote denial of service
Apache Tomcat examples directory vulnerabilities
Apache Tomcat sample files
Apache Tomcat version older than 7.0.21
Apache Tomcat version older than 7.0.23
Apache Tomcat version older than 7.0.28
Apache Tomcat version older than 7.0.30
Apache Tomcat version older than 7.0.32
Application error message
ASP.NET error message
ASP.NET version disclosure
Backup files
Basic authentication over HTTP
Blind SQL Injection
Broken links
Clickjacking: X-Frame-Options header missing
Cookie without HttpOnly flag set
Cookie without Secure flag set
Credit card number disclosed
CRLF injection/HTTP response splitting
Cross site scripting
Cross site scripting (content-sniffing)
Cross site scripting (verified)
Development configuration file
Directory listing
Documentation file
DOM-based cross site scripting
Email address found
Error message on page
Error page web server version disclosure
File inclusion
File upload
Hidden form input named price was found
Host header attack
HTML form without CSRF protection
HTTP parameter pollution
HTTP.sys remote code execution vulnerability
Insecure crossdomain.xml file
Insecure Flash embed parameter
Insecure response with wildcard '*' in Access-Control-Allow-Origin
Login page password-guessing attack
Long password denial of service
Microsoft IIS tilde directory enumeration
Microsoft IIS version disclosure
nginx SPDY heap buffer overflow
OPTIONS method is enabled
Password type input with auto-complete enabled
PHP allow_url_fopen enabled
PHP errors enabled
PHP open_basedir is not set
PHP version older than 4.3.8
PHPinfo page
Possible debug parameter found
Possible internal IP address disclosure
Possible relative path overwrite
Possible sensitive directories
Possible sensitive files
Possible server path disclosure (Unix)
Possible username or password disclosure
Possible virtual host found
RC4 cipher suites detected
Same site scripting
Server side request forgery
Session Cookie scoped to parent domain
Session fixation
Slow HTTP Denial of Service Attack
Slow response time
Snoop Servlet information disclosure
SSL 2.0 deprecated  protocol
SSL certificate invalid date
SSL certificate public key less than 2048 bit
The POODLE attack (SSLv3 supported)
TRACE method is enabled
TRACK method is enabled
URL redirection
User credentials are sent in clear text
Vulnerable Javascript library
Web Application Firewall detected
WebLogic Server Side Request Forgery
'''.splitlines()

def Add(block):#
    if block and len(block)<=250:#dict of urls
        now = datetime.datetime.now() + datetime.timedelta(minutes=+3)
        datestr = now.strftime("%m/%d/%Y")
        timestr = now.strftime("%H:%M")
        data = {"scanType": "scan",
                "targetList": "https://cdn.m.stock.pingan.com:89\nhttps://cdn.m.stock.pingan.com:80\n",
                "target": ["https://cdn.m.stock.pingan.com:89", "https://cdn.m.stock.pingan.com:80"], "recurse": "-1",
                "date": "9/28/2017", "dayOfWeek": "1", "dayOfMonth": "1", "time": "14:39",
                "deleteAfterCompletion": "True",
                "params": {"profile": "Default", "loginSeq": "<none>", "settings": "Default",
                           "scanningmode": "heuristic", "excludedhours": "<none>", "savetodatabase": "True",
                           "savelogs": "False", "generatereport": "False", "reportformat": "PDF",
                           "reporttemplate": "WVSDeveloperReport.rep", "emailaddress": ""}}
        data["targetList"] = "\n".join(block)
        data["target"] = block
        data["date"] = datestr
        data["time"] = timestr
        # print data

        header = {"RequestValidated": "true"}
        proxy = {'http': 'http://127.0.0.1:8080'}

        response = requests.post(url="http://localhost:8183/api/addScan", headers=header, json=data)
        print response.content
        if response.status_code == 200:
            return True
        else:
            return False


def AddToWVS(url_list):
    url_list = strip_list(url_list)
    start = 0
    while True:
        if len(url_list) - start >=250:
            block = url_list[start:start + 250]
            if Add(block):
                start += 250
                endindex = start
                continue
            else:
                endindex = start
                break
        elif len(url_list) - start >0:
            block = url_list[start:-1]
            if Add(block):
                endindex = start + len(block)
            else:
                endindex = start
                break
        else:
            print "Error"
    print "{0} urls added to WVS".format(endindex)
    return endindex


def QueryFromWVS(sql):
    MDB = 'C:\\ProgramData\\Acunetix WVS 10\\Data\\Database\\vulnscanresults.mdb'
    DRV = '{Microsoft Access Driver (*.mdb)}'
    PWD = 'pw'

    # connect to db
    con = pyodbc.connect('DRIVER={};DBQ={};PWD={}'.format(DRV,MDB,PWD))
    cur = con.cursor()

    rows = cur.execute(sql).fetchall()
    cur.close()
    con.close()
    return rows

if __name__ == '__main__':

    ######################################sql语句#############################################
    # 查找存在指定漏洞的URL
    specified_sql_query= '''
    select WVS_scans.starturl,WVS_alerts.algroup
     FROM WVS_alerts LEFT JOIN WVS_scans ON WVS_alerts.scid = WVS_scans.scid where algroup like '%{0}%';
     '''.format('WebLogic Server Side Request For')

    # 所有高危漏洞查询
    high_vuln_query = '''SELECT WVS_alerts.algroup, WVS_scans.starturl, Max(WVS_scans.starttime) AS starttime, WVS_alerts.severity
    FROM WVS_alerts LEFT JOIN WVS_scans ON WVS_alerts.scid = WVS_scans.scid
    WHERE (((WVS_alerts.severity)>=3))
    GROUP BY WVS_alerts.algroup, WVS_scans.starturl, WVS_alerts.severity;
    '''

    vuln_names = '''SELECT distinct WVS_alerts.algroup from WVS_alerts;'''

    ######################################sql语句#############################################
    rows = QueryFromWVS(vuln_names)
    with open('mytable.csv', 'w') as fou:
        csv_writer = csv.writer(fou) # default field-delimiter is ","
        csv_writer.writerows(rows)




