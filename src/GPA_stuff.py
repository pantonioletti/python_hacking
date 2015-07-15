# -*- coding: utf-8 -*-
__author__ = 'pantonio'
import sqlite3
import datetime
import math
from decimal import Decimal
from decimal import getcontext
from decimal import ROUND_UP
from sys import argv

import mysql.connector
import re
import GPA_Config



ROOT_EL = '<RadiantDocument CreationSource="WFM RedPrairie">'
DB_FILE = "C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\DATA\\gpa_db.db"

def insert_emp():
    sql = "INSERT INTO EMPLOYEE (JOB_STARTING_DATE,MATRICULA,STATUS,FIRST_NAME,LAST_NAME," \
                                 "PASSWORDS,LANGUAGES,CPF,BIRTH_DATE,HIRE_DATE," \
                                 "SEXO,JOB_IDENTIFIER,CCUSTO," \
                                 "DESCR_CCUSTO,DEPT,CIDADE,HPM,SECTION,SECTION_DESC) VALUES (?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?, ?,?, ?, ?, ?);"

    fd = open("C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\Data\\GPA_employees.csv",'r')
    line = fd.readline()
    count = 1
    param = list()
    while(len(line) > 0):
        line = line.replace('\n', '')
        data = line.split(",")
        job_start = None
        date = data[0].split("/")
        if (len(date[2]) == 2):
            if int(date[2]) > 15:
                y = "19"
            else:
                y = "20"
            job_start = datetime.date(int(y + date[2]), int(date[1]), int(date[0]))
        elif (len(date[2])== 4):
            job_start = datetime.date(int(date[2]),int(date[0]),int(date[1]))

        birth_date = None
        date = data[8].split("/")
        if (len(date[2]) == 2):
            birth_date = datetime.date(int("20" + date[2]), int(date[0]), int(date[1]))
        elif (len(date[2])== 4):
            birth_date = datetime.date(int(date[2]),int(date[0]),int(date[1]))

        hire_date = None
        date = data[9].split("/")
        if (len(date[2]) == 2):
            hire_date = datetime.date(int("20" + date[2]), int(date[0]), int(date[1]))
        elif (len(date[2])== 4):
            hire_date = datetime.date(int(date[2]),int(date[0]),int(date[1]))

        param.append((job_start.strftime('%Y-%m-%d'), data[1], data[2], data[3], data[4], \
                      data[5], data[6], data[7], birth_date.strftime('%Y-%m-%d'), hire_date.strftime('%Y-%m-%d'), \
                      data[10], data[11], data[12], data[13], data[14], \
                      data[15], data[16], data[17], data[18]))

        line = fd.readline()
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.executemany(sql, param)
    conn.commit()
    conn.close()

def emp_exp():
    #substr(trim(first_name),1,30), substr(trim(last_name),1,30)
    sql = "select JOB_STARTING_DATE,MATRICULA,STATUS,SUBSTR(TRIM(FIRST_NAME),1,30),SUBSTR(TRIM(LAST_NAME),1,30)," \
                  "PASSWORDS,LANGUAGES,CPF,BIRTH_DATE,HIRE_DATE," \
                  "SEXO,JOB_IDENTIFIER,CCUSTO," \
                  "DESCR_CCUSTO,DEPT,CIDADE,HPM,SECTION,SECTION_DESC from employee "\
                  "where CCUSTO = '1359' order by CCUSTO asc"
    sql_avail = "select MATRICULA, DOW, START_TIME, END_TIME " \
                "FROM EMP_AVAILABILITY "\
                "WHERE MATRICULA = '?'" \
                "ORDER BY DOW ASC"

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(sql)
    emp_data = cur.fetchall()

    #  0 - JOB_STARTING_DATE,
    #  1 - MATRICULA,
    #  2 - STATUS,
    #  3 - FIRST_NAME,
    #  4 - LAST_NAME,
    #  5 - PASSWORDS,
    #  6 - LANGUAGES,
    #  7 - CPF,
    #  8 - BIRTH_DATE,
    #  9 - HIRE_DATE,
    # 10 - SEXO,
    # 11 - JOB_IDENTIFIER,
    # 12 - CCUSTO,
    # 13 - DESCR_CCUSTO,
    # 14 - DEPT,
    # 15 - CIDADE,
    # 16 - HPM,
    # 17 - SECTION,
    # 18 - SECTION_DESC
    bu = None
    avail_time = {'0608':{1:('08:00:00','20:00:00'),2:('07:00:00','22:00:00'),3:('07:00:00','22:00:00'),4:('07:00:00','22:00:00'),5:('07:00:00','22:00:00'),6:('07:00:00','22:00:00'),7:('07:00:00','22:00:00')}, \
                  '1337':{1:('06:00:00','00:00:00'),2:('06:00:00','00:00:00'),3:('06:00:00','00:00:00'),4:('06:00:00','00:00:00'),5:('06:00:00','00:00:00'),6:('06:00:00','00:00:00'),7:('06:00:00','00:00:00')}, \
                  '1350':{1:('07:00:00','00:00:00'),2:('07:00:00','00:00:00'),3:('07:00:00','00:00:00'),4:('07:00:00','00:00:00'),5:('07:00:00','00:00:00'),6:('07:00:00','00:00:00'),7:('07:00:00','00:00:00')}, \
                  '1669':{1:('07:00:00','20:00:00'),2:('07:00:00','22:00:00'),3:('07:00:00','22:00:00'),4:('07:00:00','22:00:00'),5:('07:00:00','22:00:00'),6:('07:00:00','22:00:00'),7:('07:00:00','22:00:00')},
                  '1359':{1:('17:00:00','17:00:00'),2:('17:00:00','17:00:00'),3:('17:00:00','17:00:00'),4:('17:00:00','17:00:00'),5:('17:00:00','17:00:00'),6:('17:00:00','17:00:00'),7:('17:00:00','17:00:00')}}
    if len(emp_data)>0:
        print("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>")
        print("<EnterpriseDocument InterfaceName=\"Employee Interface\" Version=\"2.0\" CreationSource=\"WFM RedPrairie\" CreationTimestamp=\"2015-05-20T00:00:00\">")
        print("<BusinessUnitList>")
        for emp in emp_data:
            if bu != emp[12]:
                if bu is not None:
                    print("</BusinessUnit>")
                bu = emp[12]
                print("<BusinessUnit id=\"" + bu +"\">")

            print('<User id="' + emp[1] + '" statusCode="' + emp[2].lower() + '" firstName="' + emp[3] +'" lastName="' + emp[4]+ '" password="' + emp[5] + '" defaultLanguageName="' + emp[6] + '" >')
            print("<RoleList>")
            print("<Role id=\"Employee\" />")
            print("</RoleList>")
            print('<Employee ssn="' + emp[7] + '" birthDate="' + emp[8] + '" hireDate="' + emp[9] + '" gender="' + emp[10].lower() + '" managerLevelFlag="n" >')

            cur2 = conn.cursor()
            cur2.execute(sql_avail, emp[1])
            avail_data = cur2.fetchall()
            if bu in avail_time:
                 print('<Availability start="2015-01-01" end="" >')
                 print('<General dowID="1" start1="' + avail_time[bu][1][0] + '" end1="' + avail_time[bu][1][1] + '" />')
                 print('<General dowID="2" start1="' + avail_time[bu][2][0] + '" end1="' + avail_time[bu][2][1] + '" />')
                 print('<General dowID="3" start1="' + avail_time[bu][3][0] + '" end1="' + avail_time[bu][3][1] + '" />')
                 print('<General dowID="4" start1="' + avail_time[bu][4][0] + '" end1="' + avail_time[bu][4][1] + '" />')
                 print('<General dowID="5" start1="' + avail_time[bu][5][0] + '" end1="' + avail_time[bu][5][1] + '" />')
                 print('<General dowID="6" start1="' + avail_time[bu][6][0] + '" end1="' + avail_time[bu][6][1] + '" />')
                 print('<General dowID="7" start1="' + avail_time[bu][7][0] + '" end1="' + avail_time[bu][7][1] + '" />')
                 print('</Availability>')
            print("<JobList>")
            print('<Job id="' + emp[11] + '" start="' + emp[0] + '">')
            #print("<PrimaryJobInfo payPolicyId=\"Store Personnel Pay Policy\" punchRuleId=\"Store Punch Rule\" shiftStrategyId=\"Turno CLT\" />")
            punch_rule = ""
            if bu in ('0608', '1669'):
                punch_rule = '1000102'
            else:
                punch_rule = '1000101'

            print("<PrimaryJobInfo payPolicyId=\"Standard Pay Rule\" punchRuleId=\"" + punch_rule + "\" shiftStrategyId=\"Turno CLT\" />")
            print('<JobRate start="2015-01-01" rate="1.0" />')
            print("</Job>")
            print("</JobList>")
            print("</Employee>")
            print("</User>")
        print("</BusinessUnit>")
    print("</BusinessUnitList>")
    print("</EnterpriseDocument>")
    conn.close()


def emp_avail_exp():
    # substr(trim(first_name),1,30), substr(trim(last_name),1,30)
    sql = "select E.JOB_STARTING_DATE,E.MATRICULA,E.STATUS,SUBSTR(TRIM(E.FIRST_NAME),1,30),SUBSTR(TRIM(E.LAST_NAME),1,30)," \
          "E.PASSWORDS,E.LANGUAGES,E.CPF,E.BIRTH_DATE,E.HIRE_DATE," \
          "E.SEXO,E.JOB_IDENTIFIER,E.CCUSTO," \
          "E.DESCR_CCUSTO,E.DEPT,E.CIDADE,E.HPM,E.SECTION,E.SECTION_DESC, EA.DOW, EA.START_TIME, EA.END_TIME " \
          "from employee e, emp_availability ea " \
          "where E.MATRICULA = EA.MATRICULA"

    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(sql)
    emp_data = cur.fetchall()
    conn.close()

    #  0 - JOB_STARTING_DATE,
    #  1 - MATRICULA,
    #  2 - STATUS,
    #  3 - FIRST_NAME,
    #  4 - LAST_NAME,
    #  5 - PASSWORDS,
    #  6 - LANGUAGES,
    #  7 - CPF,
    #  8 - BIRTH_DATE,
    #  9 - HIRE_DATE,
    # 10 - SEXO,
    # 11 - JOB_IDENTIFIER,
    # 12 - CCUSTO,
    # 13 - DESCR_CCUSTO,
    # 14 - DEPT,
    # 15 - CIDADE,
    # 16 - HPM,
    # 17 - SECTION,
    # 18 - SECTION_DESC
    bu = None
    avail_time = {'0608': {1: ('08:00:00', '20:00:00'), 2: ('07:00:00', '22:00:00'), 3: ('07:00:00', '22:00:00'),
                           4: ('07:00:00', '22:00:00'), 5: ('07:00:00', '22:00:00'), 6: ('07:00:00', '22:00:00'),
                           7: ('07:00:00', '22:00:00')}, \
                  '1337': {1: ('06:00:00', '00:00:00'), 2: ('06:00:00', '00:00:00'), 3: ('06:00:00', '00:00:00'),
                           4: ('06:00:00', '00:00:00'), 5: ('06:00:00', '00:00:00'), 6: ('06:00:00', '00:00:00'),
                           7: ('06:00:00', '00:00:00')}, \
                  '1350': {1: ('07:00:00', '00:00:00'), 2: ('07:00:00', '00:00:00'), 3: ('07:00:00', '00:00:00'),
                           4: ('07:00:00', '00:00:00'), 5: ('07:00:00', '00:00:00'), 6: ('07:00:00', '00:00:00'),
                           7: ('07:00:00', '00:00:00')}, \
                  '1669': {1: ('07:00:00', '20:00:00'), 2: ('07:00:00', '22:00:00'), 3: ('07:00:00', '22:00:00'),
                           4: ('07:00:00', '22:00:00'), 5: ('07:00:00', '22:00:00'), 6: ('07:00:00', '22:00:00'),
                           7: ('07:00:00', '22:00:00')},
                  '1359': {1: ('17:00:00', '17:00:00'), 2: ('17:00:00', '17:00:00'), 3: ('17:00:00', '17:00:00'),
                           4: ('17:00:00', '17:00:00'), 5: ('17:00:00', '17:00:00'), 6: ('17:00:00', '17:00:00'),
                           7: ('17:00:00', '17:00:00')}}
    if len(emp_data) > 0:
        print("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>")
        print(
            "<EnterpriseDocument InterfaceName=\"Employee Interface\" Version=\"2.0\" CreationSource=\"WFM RedPrairie\" CreationTimestamp=\"2015-05-20T00:00:00\">")
        print("<BusinessUnitList>")
        for emp in emp_data:
            if bu != emp[12]:
                if bu is not None:
                    print("</BusinessUnit>")
                bu = emp[12]
                print("<BusinessUnit id=\"" + bu + "\">")

            print(
                '<User id="' + emp[1] + '" statusCode="' + emp[2].lower() + '" firstName="' + emp[3] + '" lastName="' +
                emp[4] + '" password="' + emp[5] + '" defaultLanguageName="' + emp[6] + '" >')
            print("<RoleList>")
            print("<Role id=\"Employee\" />")
            print("</RoleList>")
            print('<Employee ssn="' + emp[7] + '" birthDate="' + emp[8] + '" hireDate="' + emp[9] + '" gender="' + emp[
                10].lower() + '" managerLevelFlag="n" >')

            print('<Availability start="2015-01-01" end="" >')
            print('<General dowID="' + emp[19].__str__() + '" start1="' + emp[20] + '" end1="' + emp[21] + '" />')
            print('</Availability>')
            print("<JobList>")
            print('<Job id="' + emp[11] + '" start="' + emp[0] + '">')
            # print("<PrimaryJobInfo payPolicyId=\"Store Personnel Pay Policy\" punchRuleId=\"Store Punch Rule\" shiftStrategyId=\"Turno CLT\" />")
            punch_rule = ""
            if bu in ('0608', '1669'):
                punch_rule = '1000102'
            else:
                punch_rule = '1000101'

            print(
                "<PrimaryJobInfo payPolicyId=\"Standard Pay Rule\" punchRuleId=\"" + punch_rule + "\" shiftStrategyId=\"Turno CLT\" />")
            print('<JobRate start="2015-01-01" rate="1.0" />')
            print("</Job>")
            print("</JobList>")
            print("</Employee>")
            print("</User>")
        print("</BusinessUnit>")
    print("</BusinessUnitList>")
    print("</EnterpriseDocument>")

def txt_to_xml():
    fd = open("C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\BASE_ATIVOS_WORKFORCE.txt",'r')
    fdo = open("C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\BASE_ATIVOS_WORKFORCE.xml",'w')
    fdo.write("<?xml version=\"1.0\" encoding=\"iso-8859-1\" ?>\n")
    fdo.write("<EnterpriseDocument InterfaceName=\"Employee Interface\" Version=\"2.0\" CreationSource=\"WFM Default\" CreationTimestamp=\"2008-03-03T13:30:24\">\n")
    fdo.write("<BusinessUnitList>\n")

    getcontext().prec = 3
    getcontext().rounding = ROUND_UP
    line = fd.readline()
    emps = dict()
    stores = dict()
    count = 1
    while(len(line) != 0):
         # is not None):
        line.replace("\n","")
        dFields = line.split(';')
        if (len(dFields)<19):
            print("Fuck Off!!!! this line is incomplete " + count.__str__())
            print(line)
        else:
            # 0  JOB_STARTING_DATE
            # 1  MATRICULA
            # 2  STATUS
            # 3  FIRST_NAME
            # 4  LAST_NAME
            # 5  PASSWORDS
            # 6  LANGUAGES
            # 7  CPF
            # 8  BIRTH_DATE
            # 9  HIRE_DATE
            #10  SEXO
            #11  JOB_IDENTIFIER
            #12  ANALISE
            #13  ID_LOCAL
            #14  DESCR_LOCAL
            #15  CCUSTO
            #16  DESCR_CCUSTO
            #17  EMPR
            #18  DESCR_EMP
            if (dFields[7] in emps):
                print("FUCK!!! duplicate employees")
            else:
                emps[dFields[7]] = dFields
                st = None
                if (dFields[13] in stores):
                    st = stores[dFields[13]]
                else:
                    st = dict()
                    stores[dFields[13]]=st
                st[dFields[7]] = dFields
        line = fd.readline()
        count += 1
    for key in stores.keys():
        dStore = stores[key]
        fdo.write("<BusinessUnit id=\"" + key.replace("\"","") +"\">\n")
        for eKey in dStore.keys():
            eData = dStore[eKey]
            fdo.write("<User ")
            fdo.write("id=")
            fdo.write(eData[1])
            fdo.write(" statusCode=")
            fdo.write(eData[2].lower())
            fdo.write(" firstName=")
            fdo.write(eData[3])
            fdo.write(" lastName=")
            fdo.write(eData[4])
            fdo.write(" password=")
            fdo.write(eData[5])
            fdo.write(" defaultLanguageName=")
            fdo.write(eData[6])
            fdo.write(" >\n")
            fdo.write("<RoleList>\n")
            fdo.write("<Role id=\"Employee\" />\n")
            fdo.write("</RoleList>\n")
            fdo.write("<Employee ssn=")
            fdo.write(eData[7])
            fdo.write(" birthDate=")
            fdo.write(eData[8])
            fdo.write(" hireDate=")
            fdo.write(eData[9])
            fdo.write(" gender=")
            fdo.write(eData[10].lower())
            fdo.write(">\n")
            fdo.write("<JobList>\n")
            fdo.write("<Job id=")
            fdo.write(eData[11].replace('&','&amp;'))
            fdo.write(" start=")
            fdo.write(eData[0])
            fdo.write(">\n")
            fdo.write("<PrimaryJobInfo payPolicyId=\"Store Personnel Pay Policy\" punchRuleId=\"Store Punch Rule\" shiftStrategyId=\"Full Time\" />\n")
            fdo.write("</Job>\n")
            fdo.write("</JobList>\n")
            fdo.write("</Employee>\n")
            fdo.write("</User>\n")
        fdo.write("</BusinessUnit>\n")
    '''
                <User id="69313" statusCode="i" firstName="Diana" lastName="Morris" password="020468" defaultLanguageName="Potuguese">
                    <RoleList>
                        <Role id="Employee" />
                    </RoleList>
                    <Employee ssn="RG91827354426" birthDate="1968-04-02" hireDate="2008-01-29" gender="f">
                     <JobList>
                     <Job id="Cashier" start="2013-01-29">
                     <PrimaryJobInfo payPolicyId="Store Personnel Pay Policy" punchRuleId="Store Punch Rule" shiftStrategyId="Full Time" />
                    </Job>
                    </JobList>
                    </Employee>
                </User>
    '''


    fd.close()
    fdo.write("</BusinessUnitList>\n")
    fdo.write("</EnterpriseDocument>")
    fdo.flush()
    fdo.close()

class StoreData:
    def __init__(self, store):
        self.store = store
        self.days = dict()

class DailyData:
    def __init__(self, store, date):
        self.store = store
        self.date = date
        self.amt = Decimal(0.0)
        self.merceria_qty = 0
        self.incrments = dict()
        self.tickets = dict()

class IncrData:
    def __init__(self, time):
        self.increment = time
        self.trx_type = dict()
        self.items = 0


def parsetime(date):
    dt = date.split(" ")
    d = dt[0].split("/")
    year = int(d[2])
    month = int(d[1])
    day = int(d[0])
    t = dt[1].split(":")
    hour = int(t[0])
    mins = int(t[1])
    secs = int(t[2])
    return datetime.datetime(year, month, day, hour, mins, secs)

def parsedate(date):
    d = date.split("/")
    year = int(d[2])
    month = int(d[1])
    day = int(d[0])
    return datetime.date(year, month, day)

def parsetime(time):
    t = time.split(":")
    hour = int(t[0])
    mins = int(t[1])
    mins = 15*int(mins/15)
    secs = 0
    return datetime.time(hour, mins, secs)

def insert_stat():
    fd = open("C:\\dev\\projects\\misc\\data\\in\\GPA_trrxs_test.txt",'r')
    line = fd.readline()
    #conn = sqlite3.connect("C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\gpa_db.db")
    #cur = conn.cursor()
    count = 1
    store_data = dict()
    while(len(line) > 0):

        line = line.replace('\n', '')
        data = line.split(";")

        store = data[0]
        posid = data[1]
        date_time = parsedate(data[2])
        date = datetime.date(date_time.year, date_time.month, date_time.day)

        ticketid = data[3]
        qty = int(data[4])
        trx_type = data[5]
        merceria = data[6]
        express = data[7]
        amt = float(data[8])


        if store in store_data:
            sd = store_data[store]
        else:
            sd = StoreData(store)
            store_data[store] = sd

        if date in sd.days:
            dd = sd.days[date]
        else:
            dd = DailyData(sd.store, date)
            sd.days[date] = dd

        if ticketid not in dd.tickets:
            dd.tickets[ticketid] = amt

        if merceria == "MERCEARIA":
            dd.merceria_qty += 1
        '''stmt = "insert into raw_stats(storeid,cashierid,date,ticketid,qty,trxtype,ismerceria,isexpress,tktamt) values ("
        stmt = stmt + "'" + data[0] + "',"
        stmt = stmt + "'" + data[1] + "',"
        stmt = stmt + "strftime('" + data[2] + "'),"
        stmt = stmt + "'" + data[3] + "',"
        stmt = stmt + data[4] + ","
        stmt = stmt + "'" + data[5] + "',"
        if data[6] == "MERCEARIA":
            stmt = stmt + "1,"
        else:
            stmt = stmt + "0,"
        if data[7] == "EXPRESSA":
            stmt = stmt + "1,"
        else:
            stmt = stmt + "0,"
        stmt = stmt + data[8] + ");"
        cur.execute(stmt)
        if (count%1000 == 0):
            conn.commit()
            print(count.__str__() + " transactions inserted")
        '''
        count += 1
        line = fd.readline()
    #conn.commit()
    #print("Total transactions inserted: " + count.__str__())
    #conn.close()
    fd.close()

def process(file):
    fd = open(file,'r')
    count = 0
    line = fd.readline()
    stores = dict()
    ins_stmt = "insert into daily_sales (storeid,date,amount) values(?,?,?)"
    ins_param = list()
    while len(line)>0:
        count += 1
        line = line.replace('\n', '')  #remove new line character
        # Split by field as:
        # 0 CodLoja;
        # 1 CodCaixa;
        # 2 NumTicket;
        # 3 QtdVenda;
        # 4 DatVenda;
        # 5 FINALIZADORA;
        # 6 DIVISAO;
        # 7 TRANSACAO;
        # 8 ValTicket;
        # 9 horvenda_ini;
        #10 horvenda_fim
        data = line.split("#")

        storeid = data[0]
        ticket = data[1] + "-" + data[2]
        items_qty = Decimal(data[3])
        date = parsedate(data[4])
        trans_type = data[5]
        is_mercearia = (data[6] == 'MERCEARIA')
        tkt_amt = Decimal(data[8])
        time_incr = parsetime(data[9])

        if storeid in stores:
            store_data = stores[storeid]
        else:
            store_data = StoreData(storeid)
            stores[storeid] = store_data

        if date in store_data.days:
            daily_data = store_data.days[date]
        else:
            daily_data = DailyData(storeid, date)
            store_data.days[date] = daily_data

        if time_incr in daily_data.incrments:
            incr_data = daily_data.incrments[time_incr]
        else:
            incr_data = IncrData(time_incr)
            daily_data.incrments[time_incr] = incr_data

        if ticket not in daily_data.tickets:
            daily_data.tickets[ticket] = tkt_amt
            if trans_type in incr_data.trx_type:
                incr_data.trx_type[trans_type] += 1
            try:
                daily_data.amt = daily_data.amt + Decimal(data[8])
            except Exception as err:
                print("Exception at line: " + count.__str__())
                raise err


        incr_data.items = incr_data.items + items_qty
        if is_mercearia:
            daily_data.merceria_qty = daily_data.merceria_qty + items_qty

        line = fd.readline()

    for sid in stores.keys():
        s = stores[sid]
        for day in s.days.keys():
            d = s.days[day]
            tkt_count = len(d.tickets)
            tkt_amt = Decimal(0)
            for tkt in d.tickets.keys():
                tkt_amt = tkt_amt + d.tickets[tkt]
            print(s.store + '\t' + day.strftime('%m/%d/%y') + '\t' + tkt_count.__str__() + '\t' + tkt_amt.__str__())




    '''
            ins_param.append((sid, parsedate(day).strftime('%m/%d/%y'), daily_sales[day].__str__()))
    if len(ins_param)>0:
        conn = sqlite3.connect("C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\DATA\\gpa_db.db")
        cur = conn.cursor()
        cur.executemany(ins_stmt,ins_param)
        conn.commit()
        conn.close()
    '''
    fd.close()

def load_data_from_file():
    rep = dict((re.escape(k),v) for k, v in GPA_Config.replacements.items())
    pattern = re.compile("|".join(rep.keys()))

    conn = mysql.connector.connect(**GPA_Config.mysql_conn_str)
    stmt = "insert into trans_file (storeid,ticketid,items,date,trans_type,mercearia,amount,time_incr) values (%s,%s,%s,%s,%s,%s,%s,%s)"
    params = list()
    cur = conn.cursor()

    tot_reads = 0

    for file in GPA_Config.files2proc:
        fd = open(file,'r')
        fd.readline()
        line = fd.readline()

        count = 0
        while len(line) > 0:
            line = line.replace('.','')
            line = pattern.sub(lambda m: rep[re.escape(m.group(0))],line)
            data = line.split('\t')
            tot_reads += 1

            storeid = data[0]
            ticket = data[1] + "-" + data[2]
            items_qty = data[3]
            date = parsedate(data[4])
            trans_type = data[5]
            if data[6] == 'MERCEARIA':
                is_mercearia = 1
            else:
                is_mercearia = 0
            tkt_amt = data[8]
            time_incr = parsetime(data[9])

            params.append((storeid, ticket, items_qty, date.strftime("%Y-%m-%d"),trans_type, is_mercearia, tkt_amt, time_incr.strftime("%H:%M:%S")))
            count += 1
            if(count>=500):
                cur.executemany(stmt,params)
                conn.commit()
                count = 0
                params = list()
                #print("Total lines read: " + tot_reads.__str__())

            line = fd.readline()
        if count > 0:
            cur.executemany(stmt,params)
            conn.commit()
        print("Total lines read: " + tot_reads.__str__())
        fd.close()
    conn.close()


def just_insert_into_db(file):
    print("Start processing : " + file)
    fd = open(file,'r')
    count = 0
    line = fd.readline()
    data = list()
    stmt = "insert into trans_file (storeid,ticketid,items,date,trans_type,merecaria,amount,time_incr) values (?,?,?,?,?,?,?,?)"
    conn = sqlite3.connect(DB_FILE)
    params = list()
    while len(line)>0:
        count += 1
        line = line.replace('\n', '')  #remove new line character
        # Split by field as:
        # 0 CodLoja;
        # 1 CodCaixa;
        # 2 NumTicket;
        # 3 QtdVenda;
        # 4 DatVenda;
        # 5 FINALIZADORA;
        # 6 DIVISAO;
        # 7 TRANSACAO;
        # 8 ValTicket;
        # 9 horvenda_ini;
        #10 horvenda_fim
        data = line.split("#")

        storeid = data[0]
        ticket = data[1] + "-" + data[2]
        items_qty = data[3]
        date = parsedate(data[4])
        trans_type = data[5]
        if data[6] == 'MERCEARIA':
            is_mercearia = 1
        else:
            is_mercearia = 0
        tkt_amt = data[8]
        time_incr = parsetime(data[9])

        params.append( (storeid, ticket, items_qty, date.strftime("%Y-%m-%d"),trans_type, is_mercearia, tkt_amt, time_incr.strftime("%H:%M:%S")))

        if len(data) == 5:
            cur = conn.cursor()
            cur.executemany(stmt,params)
            conn.commit()
            count = 0
            params = list()
        line = fd.readline()

    if len(params) > 0:
        cur = conn.cursor()
        cur.executemany(stmt,params)
        conn.commit()
    conn.close()
    fd.close()

def split_by_store(file, path):
    fd = open(file,'r')
    line = fd.readline()
    store_files = dict()
    while len(line)> 0:
        #line = line.replace('\n','')
        data = line.split('#')

        if data[0] in store_files:
            fds = store_files[data[0]]
        else:
            fds = open(path+data[0]+".txt",'w')
            store_files[data[0]] = fds

        fds.write(line)
        line = fd.readline()

    for store in store_files.keys():
        store_files[store].close()

    fd.close()

class SimpleStore:
    def __init__(self, sid):
        self.id = sid
        self.days = dict()

    def addDay(self, date):
        if date not in self.days:
            self.days[date] = SimpleDay(date)

    def addIncr(self, date, time):
        self.addDay(date)
        self.days[date].addIncr(time)

    def addTrxs(self, date, time, type, count):
        self.addDay(date)
        self.days[date].addTrxs(time, type, count)

    def getData(self):
        s = list()
        for day in self.days.keys():
            s = s + self.days[day].getData(self.id)
        return s

class SimpleDay:
    def __init__(self, date):
        self.day = date
        self.incrs = dict()

    def addIncr(self, time):
        if time not in self.incrs:
            self.incrs[time] = SimpleIncr(time)

    def addTrxs(self,time, type, count):
        self.addIncr(time)
        self.incrs[time].add_trxs(type, count)

    def getData(self, store):
        s = list()
        for incr in self.incrs.keys():
            s = s + self.incrs[incr].getData(store, self.day)
        return s

class SimpleIncr:
    def __init__(self, time):
        self.incr = time
        self.trxs = dict()

    def add_trxs(self, type, count):
        if type in self.trxs:
            self.trxs[type] = self.trxs[type] + count
        else:
            self.trxs[type] = count

    def getData(self, store, date):
        s = list()
        #d = date.strftime('%m/%d/%y')
        #t = self.incr.strftime('%H:%M:%S')
        for type in self.trxs.keys():
            s.append((store, date, self.incr, type, self.trxs[type]))
        return s

def db_insert_transctions(data):
    ins_stmt = "insert into daily_transactions (storeid,date,increment,trans_type,count) values (%s,%s,%s,%s,%s)"
    if len(data)>0:
        #conn = sqlite3.connect(DB_FILE)
        conn = mysql.connector.connect(**GPA_Config.mysql_conn_str)
        cur = conn.cursor()
        cur.executemany(ins_stmt,data)
        conn.commit()
        conn.close()

def count_trxs(year, date_filter):
    store = None
    types = None

    sid = 0
    date = None

    conn = mysql.connector.connect(**GPA_Config.mysql_conn_str)
    cur = conn.cursor()

    # Gather all store/day pairs
    stmt = "select distinct storeid, date from trans_file"
    if year != 0:
        stmt += " where date like '" + year.__str__() + "%' " + date_filter
    else:
        if len(date_filter.trim()) > 0:
            stmt += date_filter.replace('and', 'where')

    cur.execute(stmt)
    st_d = cur.fetchall()
    for store_day in st_d:
        if sid != store_day[0]:
            if store is not None and len(store.days)>0:
                db_insert_transctions(store.getData())

            sid = store_day[0]
            store = SimpleStore(sid)
        date = store_day[1]
        # For every store/day gather all transactions
        cur.execute("select distinct a.ticketid, b.name, a.time_incr, b.value "
                    "from trans_file a, labor_standard b "
                    "where b.name = trans_type "
                    "and storeid = %s "
                    "and date = %s "
                    "order by a.time_incr asc, a.ticketid asc, b.value desc", store_day)
        trans = cur.fetchall()
        tkt = ""
        types = dict()
        incr = None

        for row in trans:
            #I'm counting transactions ie tickets so I consider only the first occurrence of it
            if tkt != row[0]:
                tkt = row[0]
                if incr != row[2]:
                    if incr is None:
                        incr = row[2]
                    else:
                        for type in types.keys():
                            store.addTrxs(date, incr, type, types[type])
                        types = dict()
                        incr = row[2]
                if row[1] not in types:
                    types[row[1]] = 1
                else:
                    types[row[1]] += 1

        if len(types) > 0:
            for type in types.keys():
                store.addTrxs(date, incr, type, types[type])


    if store is not None:
        if types is not None and len(types) > 0:
            for type in types.keys():
                store.addTrxs(date, incr, type, types[type])
        db_insert_transctions(store.getData())

    conn.close()

def count_transactions(year, date_filter):

    store = None
    types = None

    sid = 0
    date = None

    #conn = sqlite3.connect(DB_FILE)
    conn = mysql.connector.connect(**GPA_Config.mysql_conn_str)
    cur = conn.cursor()
    # Gather all store/day pairs
    cur.execute("select distinct storeid, date from trans_file where date like '" + year.__str__() + "%' " + date_filter)
    st_d = cur.fetchall()
    for store_day in st_d:
        if sid != store_day[0]:
            if store is not None and len(store.days)>0:
                db_insert_transctions(store.getData())

            sid = store_day[0]
            store = SimpleStore(sid)
        date = store_day[1]
        # For every store/day gather all transactions
        cur.execute("select distinct a.ticketid, b.name, a.time_incr, b.value "
                    "from trans_file a, labor_standard b "
                    "where b.name = trans_type "
                    "and storeid = %s "
                    "and date = %s "
                    "order by a.time_incr asc, a.ticketid asc, b.value desc", store_day)
        trans = cur.fetchall()
        tkt = ""
        types = dict()
        incr = None

        for row in trans:
            #I'm counting transactions ie tickets so I consider only the first occurrence of it
            if tkt != row[0]:
                tkt = row[0]
                if incr != row[2]:
                    if incr is None:
                        incr = row[2]
                    else:
                        for type in types.keys():
                            store.addTrxs(date, incr, type, types[type])
                        types = dict()
                        incr = row[2]
                if row[1] not in types:
                    types[row[1]] = 1
                else:
                    types[row[1]] += 1

        if len(types) > 0:
            for type in types.keys():
                store.addTrxs(date, incr, type, types[type])


    if store is not None:
        if types is not None and len(types) > 0:
            for type in types.keys():
                store.addTrxs(date, incr, type, types[type])
        db_insert_transctions(store.getData())

    conn.close()


def sales_exp(year, filter):

    sel_stmt = "select storeid, date_format(date,'%Y-%m-%dT00:00:00'), amount from daily_sales where date like '" + year.__str__() + "%' " + filter + " order by storeid asc, date asc"
    conn = mysql.connector.connect(**GPA_Config.mysql_conn_str)
    #conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(sel_stmt)
    s = str()
    stores = dict()
    sales = cur.fetchmany(1000)
    while len(sales)> 0 :
        for sale in sales:
            if sale[0] not in stores:
                stores[sale[0]] = list()
            stores[sale[0]].append(sale)

        sales = cur.fetchmany(1000)
    print('<RadiantDocument CreationSource="WFM RedPrairie">')
    print('<DataSet name="Generic Import" source="Actual" freq="Day">')
    for st in stores.keys():
        print('<Dimension ref_name="bu_code" value="' + st.__str__() + '">')
        print('<Metric ref_name="Total Store Sales">')
        for ds in stores[st]:
            d = ds[1]
            v = ds[2]
            print('<Data date="{0}" value="{1:.2f}"/>'.format(d,v))
        print('</Metric>')
        print('</Dimension>')

    print('</DataSet>')
    print('</RadiantDocument>')
    conn.close()

def mercearia_exp(date_filter):
    #Mercearia Itens
    sel_stmt = "select storeid, date_format(date,'%Y-%m-%dT00:00:00'), items from daily_mercearia where " + date_filter + " order by storeid asc, date asc"
    #conn = sqlite3.connect(DB_FILE)
    conn = mysql.connector.connect(**GPA_Config.mysql_conn_str)
    cur = conn.cursor()
    cur.execute(sel_stmt)
    s = str()
    stores = dict()
    mecearia = cur.fetchmany(1000)
    while len(mecearia)> 0 :
        for m in mecearia:
            if m[0] not in stores:
                stores[m[0]] = list()
            stores[m[0]].append(m)

        mecearia = cur.fetchmany(1000)
    print('<RadiantDocument CreationSource="WFM RedPrairie">')
    print('<DataSet name="Generic Import" source="Actual" freq="Day">')
    for st in stores.keys():
        print('<Dimension ref_name="bu_code" value="' + st.__str__() + '">')
        print('<Metric ref_name="Mercearia Itens">')
        for ds in stores[st]:
            d = ds[1]
            v = ds[2]
            print('<Data date="{0}" value="{1:.2f}"/>'.format(d,v))
        print('</Metric>')
        print('</Dimension>')

    print('</DataSet>')
    print('</RadiantDocument>')
    conn.close()

def items_exp(year, str_filter, date_filter):
    print ('<RadiantDocument CreationSource="WFM RedPrairie">')
    print('<DataSet name="Generic Import" source="Actual" freq="QuarterHour">')

    stmt = "select distinct storeid from daily_items where date like '" + year.__str__() +  "%' " + str_filter + " " + date_filter
    conn = mysql.connector.connect(**GPA_Config.mysql_conn_str)
    #sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(stmt)
    stores = cur.fetchall()

    stmt = "select concat(date_format(date,'%Y-%m-%d'),'T',time_incr) dt, items " \
            "from daily_items " \
            "where storeid = %s "
    if len(date_filter) > 0:
        stmt = stmt + date_filter
    else:
        stmt = stmt + "and date like '" + year.__str__() + "%' "
    stmt += "order by dt"

    for store in stores:
        cur.execute(stmt, store)
        data = cur.fetchall()
        print('<Dimension ref_name="bu_code" value="' + store[0].__str__() + '">')
        print('<Metric ref_name="Itens">')
        for d in data:
            print('<Data date="{0}" value="{1:.2f}"/>'.format(d[0],d[1]))
        print('</Metric>')
        print('</Dimension>')
    print('</DataSet>')
    print ('</RadiantDocument>')
    conn.close()

def dinheiro_exp(date_filter):
    print ('<RadiantDocument CreationSource="WFM RedPrairie">')
    print('<DataSet name="Generic Import" source="Actual" freq="QuarterHour">')

    stmt = "select distinct storeid from daily_cash where " + date_filter
    conn = mysql.connector.connect(**GPA_Config.mysql_conn_str)
    #conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(stmt)
    stores = cur.fetchall()

    stmt = "select concat(date_format(date,'%Y-%m-%d'),'T',time_incr) dt, cash_amt " \
            "from daily_cash " \
            "where storeid = %s " \
            "and " + date_filter + " "\
            "order by dt"

    for store in stores:
        cur.execute(stmt, store)
        data = cur.fetchall()
        print('<Dimension ref_name="bu_code" value="' + store[0].__str__() + '">')
        print('<Metric ref_name="Dinheiro Ventas">')
        for d in data:
            print('<Data date="{0}" value="{1:.2f}"/>'.format(d[0],d[1]))
        print('</Metric>')
        print('</Dimension>')
    print('</DataSet>')
    print ('</RadiantDocument>')
    conn.close()

def trxs_exp(date_filter):

    fd = open(GPA_Config.out_file, mode='w', encoding='utf-8')
    fd.write ('<?xml version="1.0" encoding="UTF-8"?>\n')
    fd.write ('<RadiantDocument CreationSource="WFM RedPrairie">\n')
    fd.write('<DataSet name="Generic Import" source="Actual" freq="QuarterHour">\n')

    stmt = "select distinct storeid from daily_transactions where " + date_filter
    conn = mysql.connector.connect(**GPA_Config.mysql_conn_str)
    #conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(stmt)
    stores = cur.fetchall()

    stmt1 = "select distinct trans_type " \
            "from daily_transactions " \
            "where storeid = %s " \
            "and " + date_filter

    stmt2 = "select concat(date_format(date,'%Y-%m-%d'),'T',increment) dt, count " \
            'from daily_transactions ' \
            'where storeid = %s ' \
            "and " + date_filter + " " \
            'and trans_type = %s ' \
            'order by dt'

    for store in stores:
        fd.write('<Dimension ref_name="bu_code" value="' + store[0].__str__() + '">\n')
        cur.execute(stmt1, store)
        trxs = cur.fetchall()
        for t in trxs:
            cur.execute(stmt2,(store[0],t[0]))
            fd.write('<Metric ref_name="' + t[0] + '">\n')
            data = cur.fetchall()
            for d in data:
                fd.write('<Data date="{0}" value="{1:.0f}"/>\n'.format(d[0],d[1]))
            fd.write('</Metric>\n')
        fd.write('</Dimension>\n')
    fd.write('</DataSet>\n')
    fd.write ('</RadiantDocument>')
    conn.close()
    fd.close()


def trxs_exp2(date_filter):
    fd = open(GPA_Config.out_file, mode='w', encoding='utf-8')
    fd.write ('<?xml version="1.0" encoding="UTF-8"?>\n')
    fd.write ('<RadiantDocument CreationSource="WFM RedPrairie">\n')
    fd.write('<DataSet name="Generic Import" source="Actual" freq="QuarterHour">\n')

    stmt = "select distinct storeid from daily_transactions where " + date_filter
    #conn = sqlite3.connect(DB_FILE)
    conn = mysql.connector.connect(**GPA_Config.mysql_conn_str)
    cur = conn.cursor()
    cur.execute(stmt)
    stores = cur.fetchall()

    stmt2 = "select concat(date_format(date,'%Y-%m-%d'),'T',increment) dt, sum(count) " \
            'from daily_transactions ' \
            'where storeid = %s ' \
            "and " + date_filter + " " \
            "group by date, increment " \
            'order by dt'

    for store in stores:
        fd.write('<Dimension ref_name="bu_code" value="' + store[0].__str__() + '">\n')
        cur.execute(stmt2,(store))
        fd.write('<Metric ref_name="Transacao">\n')
        data = cur.fetchall()
        for d in data:
            fd.write('<Data date="{0}" value="{1:.0f}"/>\n'.format(d[0],d[1]))
        fd.write('</Metric>\n')
        fd.write('</Dimension>\n')
    fd.write('</DataSet>\n')
    fd.write ('</RadiantDocument>\n')
    conn.close()
    fd.close()

def calc_sales(date_filter):

    stmt = "insert into daily_sales (storeid, date, amount)" \
           "select tf.storeid, tf.date, sum(tf.amount) " \
           "from (select distinct storeid, ticketid, date, amount " \
           "from trans_file " \
           "where " + date_filter + ") tf " \
           "group by tf.storeid, tf.date"

    conn = mysql.connector.connect(**GPA_Config.mysql_conn_str)
    #conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(stmt)
    conn.commit()
    conn.close()

def calc_items(filter):

    stmt = "insert into daily_items (storeid, date, time_incr, items) " \
           "select storeid, date, time_incr, sum(items) " \
           "from trans_file " \
           "where " + filter + " " \
           "group by storeid, date, time_incr"

    conn = mysql.connector.connect(**GPA_Config.mysql_conn_str)
    #conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(stmt)
    conn.commit()
    conn.close()

def calc_mercearia(filter):

    stmt = "insert into daily_mercearia (storeid, date, items) " \
           "select storeid, date, sum(items) " \
           "from trans_file " \
           "where "+filter+" " \
           "and mercearia = '1' " \
           "group by storeid, date"


    conn = mysql.connector.connect(**GPA_Config.mysql_conn_str)
    #conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(stmt)
    conn.commit()
    conn.close()

def calc_cash(filter):

    stmt = "insert into daily_cash (storeid, date, time_incr, cash_amt) " \
           "select cs.storeid, cs.date, cs.time_incr, sum(cs.amount) " \
           "from (select distinct storeid, date, time_incr, ticketid, amount " \
           "from trans_file " \
           "where "+filter+" " \
           "and   trans_type = 'Transacao Dinheiro') cs " \
           "group by cs.storeid, cs.date, cs.time_incr"


    conn = mysql.connector.connect(**GPA_Config.mysql_conn_str)
    #conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute(stmt)
    conn.commit()
    conn.close()


getcontext().prec = 2
getcontext().rounding = ROUND_UP



if GPA_Config.exec_cmd == 'sales':
    sales_exp(2015,"and date > '2015-06-28'")
elif GPA_Config.exec_cmd == 'file_import':
    load_data_from_file()
elif GPA_Config.exec_cmd == 'items':
    items_exp(2015,"and storeid in ('1337', '1350', '1359','1669', '0608') ", "and date > '2015-06-21' ")
elif GPA_Config.exec_cmd == 'count_trxs':
    count_trxs(2015, "and date > '2015-06-06' ")
elif GPA_Config.exec_cmd == 'trx_det':
    trxs_exp("date > '2015-06-28' ")
elif GPA_Config.exec_cmd == 'trx_tot':
    trxs_exp2("date > '2015-06-06' ")
elif GPA_Config.exec_cmd == 'mercearia':
    mercearia_exp("date > '2015-06-06' ")
elif GPA_Config.exec_cmd == 'cash':
    dinheiro_exp("date > '2015-06-06' ")
elif GPA_Config.exec_cmd == 'calc_sales':
    calc_sales("date > '2015-06-28' and storeid in ('0608','1669') ")
elif GPA_Config.exec_cmd == 'calc_items':
    calc_items(" date > '2015-06-28'")
    #storeid in ('1337', '1350', '1359', '1669', '0608') " \
elif GPA_Config.exec_cmd == 'calc_mercearia':
    calc_mercearia(" date > '2015-06-28'")
    #storeid in ('1337', '1350', '1359', '1669', '0608') " \
    #       "and date >= '2015-05-19'
elif GPA_Config.exec_cmd == 'calc_cash':
    calc_mercearia(" date > '2015-06-28'")
exit(1)



#print(file)
#insert_emp()
#insert_stat()

#emp_avail_exp()

#Use it to split a file by an inside criteria
#split_by_store(argv[1],argv[2])
#exit(0)





#Step 1 - load files
'''
#if len(argv) < 2:
#    print("Give the file name to process")
#else:
#    fdp = open(argv[1])
#    file_path = fdp.readline()
for fp in GPA_Config.filestoproc:
    just_insert_into_db(fp)
    #while len(file_path) > 0:
    #    file_path = file_path.replace('\n','')
    #    #process(file_path)
    #    just_insert_into_db(file_path)
    #    file_path = fdp.readline()
    #fdp.close()
'''

#Step 2: run SQL to consolidate sales in daily_sales table
'''
insert into daily_sales (storeid, date, amount)
select storeid, date, sum(amount) from (
select distinct storeid, ticketid, date, amount
from trans_file
where storeid = '0608')
group by storeid, date;
'''

#Step 3: export sales
#sales_exp(2015,"and storeid in ('1337', '1350', '1359') and date > '2015-05-18'")

#Step 4: eun SQL to consolidate items in daily_items table
'''
insert into daily_items (storeid, date, time_incr, items)
select storeid, date, time_incr, sum(items)
from trans_file
where storeid in ('1337', '1350', '1359', '1669', '0608')
and date like '2013%'
group by storeid, date, time_incr;
'''
#Step 5: export Items
#items_exp(2015,"and storeid in ('1337', '1350', '1359') ", "and date > '2015-05-18' ")

#Step 6: count transaction by type by 15 min increments
#count_transactions(2015, "and date > '2015-05-18' ")

#Step7: export transaction by type by 15 min increments
#trxs_exp("date > '2015-05-18' ")
#trxs_exp2("date > '2015-05-18' ")

#Step8: count items for mercearia
'''
insert into daily_mecearia (storeid, date, items)
select storeid, date, sum(items)
from trans_file
where storeid in ('1337', '1350', '1359', '1669', '0608')
and date like '2015%'
and merecaria = 1
group by storeid, date, time_incr
'''
#Step 9: export mercearia
#mercearia_exp("date > '2015-05-18' ")

#Step 10: calc sales
'''
insert into daily_cash (storeid, date, time_incr, cash_amt)
select storeid, date, time_incr, sum(amount)
from
(select distinct storeid, date, time_incr, ticketid, amount
from trans_file
where trans_type = 'Transacao Dinheiro'
and date > '2015-05-18'
)
group by storeid, date, time_incr;
'''
#Step 11: export Dinheiro Ventas
#dinheiro_exp("date > '2015-05-18' ")