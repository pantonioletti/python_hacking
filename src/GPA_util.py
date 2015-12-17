__author__ = 'pantonio'

import datetime
import re
from sys import argv

def parsedate(date):
    d = date.split("/")
    year = int(d[2])
    month = int(d[1])
    day = int(d[0])
    return datetime.date(year, month, day)

def gpa2pg(filename):
    replacements={'\n':'',',':'.'}
    rep = dict((re.escape(k),v) for k, v in replacements.items())
    pattern = re.compile("|".join(rep.keys()))
    fd = open(filename,'r')
    line = fd.readline()
    if line.startswith('CodLoja'):
        line = fd.readline()
    while len(line)>0:
        line = line.replace('.','')
        line = pattern.sub(lambda m: rep[re.escape(m.group(0))],line)
        data = line.split('\t')
        print('{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10}'.format(data[0],data[1],parsedate(data[2]),data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10]))
        line = fd.readline()
    fd.close()

cmd = argv[1]

if cmd == 'convert':
    gpa2pg(argv[2])
elif cmd == 'sftp':

    import paramiko
    import pysftp

    conn = pysftp.Connection(host='PREPB2BGW01.JDADELIVERS.COM',private_key='C:\\dev\\apps\\putty\\GPA.ppk',username='gpawmdldevi')
    print(conn.pwd)