__author__ = 'pantonio'

import httplib2
import urllib.parse
import json
from sys import argv

def login(user, passwd, url):
    h = httplib2.Http(".cache")
    body = {'loginName':user, 'password':passwd}
    headers = {'Content-type': 'application/x-www-form-urlencoded'}
    resp0, content0 = h.request(url,'POST',headers=headers,body=urllib.parse.urlencode(body))
    cookie = resp0['set-cookie']
    return h, cookie

def usr_to_rem(file_path, prefix):
    fd = open(file_path,'r')
    line = fd.readline()
    d_users= dict()
    while len(line) > 0:
        line = line.replace('\n','')
        data = line.split(';')
        if len(data)>1:
            d_users[data[0]] = prefix+data[1]
        line = fd.readline()
    fd.close()
    return d_users

def update_login_name(headers, users, active,h):
    url=''
    body=dict()
    resp1=dict()
    for usr in users.keys():
        url = 'http://dlgpadeva1v.jdadelivers.com/retail/data/retailwebapi/api/v1-beta2/Users/'+usr+'/loginChange'
        body = {"ID":1,"LoginName": users[usr],"IsLoginActive":active}
        body_jason = json.dumps(body)
        resp1, content1 = h.request(url,'PUT',headers=headers,body=body_jason)
        if resp1['refs-status'] != '0':
            print('ERROR processing=> user_id: {0} ||  login_name: {1}'.format(usr, users[usr]))
            print(resp1.__str__())

def update_wf_emp(headers, users, h):
    url = 'http://dlgpadeva1v.jdadelivers.com/retail/data/retailwebapi/api/v1-beta2/EmployeeStatuses?autoResolveTransactionalData=true'
    body = {"ID": 1,
            "IsActive": False,
            "EmployeeStatusCode": "Separate",
            "Start": "2015-10-01T00:00:00",
            "EligibleForRehire": False,
            "Employee":{"Rel":"employee","Method":"GET","Uri":"employees/1"}}
    for usr in users.keys():
        body["EmployeeID"] = usr
        body["HomeSiteID"] = users[usr]
        body_json = json.dumps(body)
        resp1, content1 = h.request(url,'POST',headers=headers,body=body_json)
        if resp1['refs-status'] != '0':
            print('ERROR processing=> user_id: {0} ||  login_name: {1}'.format(usr, users[usr]))
            print(resp1.__str__())

def get_badge_number(headers, users):
    dbn2upd=dict()
    for usr in users.keys():
        url = 'http://dlgpadeva1v.jdadelivers.com/retail/data/retailwebapi/api/v1-beta2/Employees/'+usr
        #body = {"ID":1,"LoginName": users[usr],"IsLoginActive":False}
        #body_jason = json.dumps(body)
        resp1, content1 = h.request(url,'GET',headers=headers)
        if resp1['refs-status'] != '0':
            print(resp1.__str__())
        else:
            dbn2upd[usr]=content1["BadgeNumber"]

#First of all: login
login_url = 'http://dlgpadeva1v.jdadelivers.com/retail/data/login'
h, cookie = login('PAntonioletti','1QAZXSW2',login_url)
headers=dict()
headers['Cookie'] = cookie
headers['Content-type'] = 'application/json'

l_users = usr_to_rem(argv[1],'')
update_wf_emp(headers,l_users, h)
