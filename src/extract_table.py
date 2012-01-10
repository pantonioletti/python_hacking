#coding=UTF-8
'''
Created on Nov 24, 2010

@author: pantonio
'''

def extract_table(query):
    lq = query.lower()
    s = lq.find('from')
    tables = ''
    if s > -1:
        e = lq.find('where', s+4)
        if e == -1:
            tables = lq[s+4:]
        else:
            tables = lq[s+4:e]
    return tables

fd = open('C:/temp/selects.log', 'r')
str = fd.readline()
dt = set()
while len(str)!= 0:
    str = str.replace('\n', '')
    t = extract_table(str)
    if (len(t)>0):
        tt = t.rsplit(',')
        for st in tt[:]:
            st = st.strip()
            idx = st.find(' ')
            if idx > -1:
                st = st[:idx]
            dt.add(st)
    str = fd.readline()
while(len(dt)> 0):
    print(dt.pop())
    
