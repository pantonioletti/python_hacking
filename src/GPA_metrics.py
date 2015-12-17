# -*- coding: utf-8 -*-
__author__ = 'pantonio'

import datetime
from decimal import Decimal
from sys import argv
from os import listdir
from os.path import exists
from os.path import isfile
import psycopg2
import GPA_Config
import re
from time import time

B_CTL=2**9
B_TOT=B_CTL|(2**8)
B_SVC=B_CTL|(2**7)
B_MER=B_CTL|(2**6)
B_CART=B_CTL|(2**5)
B_CSH=B_CTL|(2**4)
B_CHQ=B_CTL|(2**3)
B_CANC=B_CTL|(2**2)
B_COB=B_CTL|(2**1)
B_DIV=B_CTL|(2**0)

MTR_NAME_SALES = ('Vendas','{0}\\GPA_SALES_{1:.0f}.xml')
MTR_NAME_MERCEARIA = ('Mercearia Itens','{0}\\GPA_MERCEARIA_{1:.0f}.xml')
MTR_NAME_SVCS = ('Servico','{0}\\GPA_SVCS_{1:.0f}.xml')
MTR_NAME_CASH_AMT = ('Dinheiro Vendas','{0}\\GPA_CASH_AMT_{1:.0f}.xml')
MTR_NAME_SCANS = ('Lancamentos','{0}\\GPA_SCANS_{1:.0f}.xml')
MTR_NAME_CANCEL = ('Cancelado','{0}\\GPA_CANCEL_{1:.0f}.xml')
MTR_NAME_DCCARD = ('Transacao Cartao','{0}\\GPA_DCCARD_{1:.0f}.xml')
MTR_NAME_CHCK = ('Transacao Cheque','{0}\\GPA_CHECK_{1:.0f}.xml')
MTR_NAME_COV = ('Cobertura','{0}\\GPA_COV_{1:.0f}.xml')
MTR_NAME_TCASH = ('Transacao Dinheiro','{0}\\GPA_TCASH_{1:.0f}.xml')
MTR_NAME_DIV = ('Divergencia','{0}\\GPA_DIV_{1:.0f}.xml')

TRX_CASH="DINHEIRO"
TRX_CCARD="CARTAO"
TRX_CHECK="CHEQUE"
TRX_SVCS="SERVICOS"
TRX_CANCEL="CANCELADOS"
TRX_COV="COBERTURA"
TRX_DIV="DIVERGENCIA"
TRX_MERCE="MERCEARIA"
TRX_TOT="TOTAL"

replacements={'\n':'',',':'.'}


ROOT_EL = '<RadiantDocument CreationSource="GPA">\n<DataSet name="Generic Import" source="Actual" freq="{0}">\n'
ROOT_CLOSE = '</DataSet>\n</RadiantDocument>\n'
DIMENSION_EL = '<Dimension ref_name="bu_code" value="{0}">\n'
DIMENSION_CLOSE = '</Dimension>\n'
METRIC_EL = '<Metric ref_name="{0}">\n'
METRIC_CLOSE = '</Metric>\n'

def get_files(inpath):
    l_to_proc = list()
    if exists(inpath): #Verify correctness of paths
        l_files = listdir(inpath) #Get all files in inpath
        for file in l_files:
            f_full_name= inpath+'\\'+file
            if (file.endswith(".txt") and isfile(f_full_name)): # Verify if it's file
                l_to_proc.append(f_full_name)
    return l_to_proc

'''
    Read all files in inpath params and rewrite
    data to temp files in tmppath by store
'''
def break_down_files(inpath, tmppath):

    ltmp_files = list()
    if exists(inpath) and exists(tmppath): #Verify correctness of paths
        lst_files = listdir(inpath) #Get all files in inpath
        for file in lst_files:
            f_full_name= inpath+'\\'+file
            if (file.endswith(".txt") and isfile(f_full_name)): # Verify if it's file
                dstr_file = dict() # Dictionary of (storeid, file descriptor)
                fd = open(f_full_name,'r')
                line = fd.readline()
                if len(line)>0 and line.startswith("CodLoja"):
                    line = fd.readline()
                while (len(line)>0):
                    t_pos=line.find('\t',0)
                    if t_pos > 0:
                        data = line[0:t_pos]
                        if data not in dstr_file:#If store id is not in dictionary
                            tmp_file_name = '{0}\\tmp_{1}_{2:.0f}.txt'.format(tmppath, data, time())
                            dstr_file[data] = open(tmp_file_name,'w') #Open a file for this
                            ltmp_files.append(tmp_file_name)
                        dstr_file[data].write(line)
                    line = fd.readline()
                for key in dstr_file.keys():
                    dstr_file[key].close()
                fd.close()
    return ltmp_files

def print_daily_metric(exp_path, d_data, s_name):
    f_exp = open(exp_path, 'w')
    f_exp.write(ROOT_EL.format('Day'))
    for store_id in d_data.keys():
        f_exp.write(DIMENSION_EL.format(store_id))
        f_exp.write(METRIC_EL.format(s_name))
        for date in d_data[store_id].keys():
            f_exp.write('<Data date="{0}T00:00:00" value="{1:.2f}"/>\n'.format(date,d_data[store_id][date]))
        f_exp.write(METRIC_CLOSE)
        f_exp.write(DIMENSION_CLOSE)
    f_exp.write(ROOT_CLOSE)
    f_exp.close()
    f_exp = open(exp_path+'.flag', 'w')
    f_exp.close()

def print_15min_metric(exp_path, d_data, s_name):
    f_exp = open(exp_path, 'w')
    f_exp.write(ROOT_EL.format('QuarterHour'))
    for store_id in d_data.keys():
        if (len(d_data[store_id])):
            f_exp.write(DIMENSION_EL.format(store_id))
            f_exp.write(METRIC_EL.format(s_name))
            for date in d_data[store_id].keys():
                for time_incr in d_data[store_id][date]:
                    f_exp.write('<Data date="{0}T{1}" value="{2:.2f}"/>\n'.format(date,time_incr, d_data[store_id][date][time_incr]))
            f_exp.write(METRIC_CLOSE)
            f_exp.write(DIMENSION_CLOSE)
    f_exp.write(ROOT_CLOSE)
    f_exp.close()
    f_exp = open(exp_path+'.flag', 'w')
    f_exp.close()
'''
	Line structure:
	0 store id
	1 POS id
	2 date
	3 transaction type
	4 amount
	5 # of transactions
	6 # of scans
	7 # of items
	8 start time
	9 end time
	10 ticket number
'''
def calculate_metrics(lfiles,outpath):
    timestamp = '%.0f'%time()
    rep = dict((re.escape(k),v) for k, v in replacements.items())
    pattern = re.compile("|".join(rep.keys()))
    d_str=dict()
    d_sales = dict()
    d_mercearia = dict()
    d_svcs = dict()
    d_cash_money = dict()
    d_scans = dict()
    d_ccard = dict()
    d_cash = dict()
    d_check = dict()
    d_cancel = dict()
    d_div = dict()
    d_cov = dict()
    for file in lfiles:
        fd = open(file,'r')
        line = fd.readline()
        if len(line)>0 and line.startswith("CodLoja"):
            line = fd.readline()
        while len(line) > 0:
            line = line.replace('.','')
            line = pattern.sub(lambda m: rep[re.escape(m.group(0))],line)
            data = line.split('\t')
            store_id = data[0]
            date = parsedate(data[2]).__str__()
            time_incr = parsetime(data[8]).__str__()
            tckt_id = date + data[1] + data[10]
            tckt_chk = B_CTL
            if store_id not in d_str:
                d_str[store_id] = dict()
                d_sales[store_id] = dict()
                d_mercearia[store_id] = dict()
                d_svcs[store_id] = dict()
                d_cash_money[store_id] = dict()
                d_scans[store_id] = dict()
                d_ccard[store_id] = dict()
                d_cash[store_id] = dict()
                d_check[store_id] = dict()
                d_cancel[store_id] = dict()
                d_div[store_id] = dict()
                d_cov[store_id] = dict()

            if tckt_id not in d_str[store_id]:
                d_str[store_id][tckt_id] = tckt_chk
            else:
                tckt_chk = d_str[store_id][tckt_id]

            if date not in d_sales[store_id]:
                d_sales[store_id][date] = Decimal(0.0)

            t_type = data[3]
            if t_type == TRX_TOT:
                if tckt_chk&B_SVC!=B_CTL:
                    print("ERROR: services ticket has products")
                d_sales[store_id][date] += Decimal(data[4])
                if date not in d_scans[store_id]:
                    d_scans[store_id][date]= dict()
                if time_incr not in d_scans[store_id][date]:
                    d_scans[store_id][date][time_incr] = Decimal(data[6])
                else:
                    d_scans[store_id][date][time_incr] += Decimal(data[6])
                tckt_chk |= B_TOT
            elif t_type == TRX_SVCS:
                if tckt_chk&B_TOT!=B_CTL:
                    print("ERROR: products ticket has service ")
                if date not in d_svcs[store_id]:
                    d_svcs[store_id][date]= dict()
                if time_incr not in d_svcs[store_id][date]:
                    d_svcs[store_id][date][time_incr] = 1
                else:
                    d_svcs[store_id][date][time_incr] += 1
                tckt_chk |= B_SVC
            elif t_type == TRX_MERCE:
                if tckt_chk&B_SVC!=B_CTL:
                    print("ERROR: services ticket has products (Mercearia)")
                if date not in d_mercearia[store_id]:
                    d_mercearia[store_id][date] = Decimal(data[7])
                else:
                    d_mercearia[store_id][date] += Decimal(data[7])
                tckt_chk |= B_MER
            elif t_type == TRX_CASH:
                if date not in d_cash_money[store_id]:
                    d_cash_money[store_id][date]= dict()
                    d_cash[store_id][date]= dict()
                if time_incr not in d_cash_money[store_id][date]:
                    d_cash_money[store_id][date][time_incr] = Decimal(data[4])
                    d_cash[store_id][date][time_incr] = 1
                else:
                    d_cash_money[store_id][date][time_incr] += Decimal(data[4])
                    d_cash[store_id][date][time_incr] += 1
                tckt_chk |= B_CSH
            elif t_type == TRX_CCARD:
                if date not in d_ccard[store_id]:
                    d_ccard[store_id][date]= dict()
                if time_incr not in d_ccard[store_id][date]:
                    d_ccard[store_id][date][time_incr] = 1
                else:
                    d_ccard[store_id][date][time_incr] += 1
                tckt_chk |= B_CART
            elif t_type == TRX_CHECK:
                if date not in d_check[store_id]:
                    d_check[store_id][date]= dict()
                if time_incr not in d_check[store_id][date]:
                    d_check[store_id][date][time_incr] = 1
                else:
                    d_check[store_id][date][time_incr] += 1
                tckt_chk |= B_CHQ
            elif t_type == TRX_CANCEL:
                if tckt_chk&B_SVC!=B_CTL:
                    print("ERROR: services ticket has products (Cancelamento)")
                if date not in d_cancel[store_id]:
                    d_cancel[store_id][date]= dict()
                if time_incr not in d_cancel[store_id][date]:
                    d_cancel[store_id][date][time_incr] = 1
                else:
                    d_cancel[store_id][date][time_incr] += 1
                tckt_chk |= B_CANC
            elif t_type == TRX_COV:
                if tckt_chk&B_SVC!=B_CTL:
                    print("ERROR: services ticket has products (Cobertura)")
                if date not in d_cov[store_id]:
                    d_cov[store_id][date]= dict()
                if time_incr not in d_cov[store_id][date]:
                    d_cov[store_id][date][time_incr] = Decimal(data[5])
                else:
                    d_cov[store_id][date][time_incr] += Decimal(data[5])
                tckt_chk |= B_COB
            elif t_type == TRX_DIV:
                if tckt_chk&B_SVC!=B_CTL:
                    print("ERROR: services ticket has products (Divergencia)")
                if date not in d_div[store_id]:
                    d_div[store_id][date]= dict()
                if time_incr not in d_div[store_id][date]:
                    d_div[store_id][date][time_incr] = Decimal(data[5])
                else:
                    d_div[store_id][date][time_incr] += Decimal(data[5])
                tckt_chk |= B_DIV
            d_str[store_id][tckt_id]=tckt_chk
            line = fd.readline()
        fd.close()
        #remove(file)

    if len(d_sales) > 0:
        print_daily_metric(MTR_NAME_SALES[1].format(outpath, time()), d_sales, MTR_NAME_SALES[0])

    if len(d_mercearia)> 0:
        print_daily_metric(MTR_NAME_MERCEARIA[1].format(outpath, time()), d_mercearia, MTR_NAME_MERCEARIA[0])

    if len(d_svcs)> 0:
        print_15min_metric(MTR_NAME_SVCS[1].format(outpath, time()), d_svcs, MTR_NAME_SVCS[0])

    if len(d_cash_money)> 0:
        print_15min_metric(MTR_NAME_CASH_AMT[1].format(outpath, time()), d_cash_money, MTR_NAME_CASH_AMT[0])

    if len(d_scans)> 0:
        print_15min_metric(MTR_NAME_SCANS[1].format(outpath, time()), d_scans, MTR_NAME_SCANS[0])

    if len(d_cash)> 0:
        print_15min_metric(MTR_NAME_TCASH[1].format(outpath, time()), d_cash, MTR_NAME_TCASH[0])

    if len(d_ccard)> 0:
        print_15min_metric(MTR_NAME_DCCARD[1].format(outpath, time()), d_ccard, MTR_NAME_DCCARD[0])

    if len(d_check)> 0:
        print_15min_metric(MTR_NAME_CHCK[1].format(outpath, time()), d_check, MTR_NAME_CHCK[0])

    if len(d_cancel)> 0:
        print_15min_metric(MTR_NAME_CANCEL[1].format(outpath, time()), d_cancel, MTR_NAME_CANCEL[0])

    if len(d_div)> 0:
        print_15min_metric(MTR_NAME_DIV[1].format(outpath, time()), d_div, MTR_NAME_DIV[0])

    if len(d_cov)> 0:
        print_15min_metric(MTR_NAME_COV[1].format(outpath, time()), d_cov, MTR_NAME_COV[0])

'''
Parses a date-time string in format "dd/mm/yyyy hh:mi:ss"
'''
def parsedatetime(date):
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

'''
Parses a date string in format "dd/mm/yyyy"
'''
def parsedate(date):
    d = date.split("/")
    year = int(d[2])
    month = int(d[1])
    day = int(d[0])
    return datetime.date(year, month, day)

'''
Parses a time string in format "hh:mi:ss"
'''
def parsetime(time):
    t = time.split(":")
    hour = int(t[0])
    mins = int(t[1])
    mins = 15*int(mins/15)
    secs = 0
    return datetime.time(hour, mins, secs)
'''
Calculates time difference assuming start and end time could be
on different days (no more than one)
'''
def difftime():
    start=datetime.time()
    end=datetime.time()
    if end.hour < start.hour:
        hour = end.hour + 24 - start.hour
        mins = end.mins + 60 - start.mins
        secs = end.second + 60 - start.second
        if secs > 59:
            secs = 60 - secs
            mins += 1
        if mins > 59:
            mins = 60 - mins
            hour += 1
    else:
        hour = end.hour - start.hour
        if end.minute < start.minute:
            mins = end.minute + 60 - start.minute
            hour -= 1
        if end.second < start.second:
            secs = end.second + 60 - start.second
            mins -= 1

'''
Export to XML file daily sales data
'''
def sales_exp(filter, of):

    sel_stmt = "select storeid, to_char(date,'YYYY-MM-DDT00:00:00'), amount "\
               "from daily_sales "\
               "where " + filter + " order by storeid asc, date asc"

    conn = conn = psycopg2.connect(host=GPA_Config.pgsql_conn_str["host"], \
                            port=GPA_Config.pgsql_conn_str["port"], \
                            database=GPA_Config.pgsql_conn_str["database"], \
                            user=GPA_Config.pgsql_conn_str["user"], \
                            password=GPA_Config.pgsql_conn_str["password"])

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

    if len(stores) > 0:
        fd = open(of, mode='w', encoding='utf-8')

        fd.write(ROOT_EL)
        fd.write('<DataSet name="Generic Import" source="Actual" freq="Day">')
        for st in stores.keys():
            fd.write('<Dimension ref_name="bu_code" value="' + st.__str__() + '">')
            fd.write('<Metric ref_name="Vendas">')
            for ds in stores[st]:
                d = ds[1]
                v = ds[2]
                fd.write('<Data date="{0}" value="{1:.2f}"/>'.format(d,v))
            fd.write('</Metric>')
            fd.write('</Dimension>')

        fd.write('</DataSet>')
        fd.write('</RadiantDocument>')
        conn.close()
        fd.close()
        fd = open(of+".flag", mode='w')
        fd.close()

'''
Export to XML file daily mercearia invetory sold units data
'''
def mercearia_exp(date_filter, of):
    #Mercearia Itens
    sel_stmt = "select storeid, to_char(date,'YYYY-MM-DDT00:00:00'), items "\
               "from daily_mercearia "\
               "where " + date_filter + " order by storeid asc, date asc"
    conn = conn = psycopg2.connect(host=GPA_Config.pgsql_conn_str["host"], \
                            port=GPA_Config.pgsql_conn_str["port"], \
                            database=GPA_Config.pgsql_conn_str["database"], \
                            user=GPA_Config.pgsql_conn_str["user"], \
                            password=GPA_Config.pgsql_conn_str["password"])

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

    if len(stores) > 0:
        fd = open(of, mode='w', encoding='utf-8')

        fd.write(ROOT_EL)
        fd.write('<DataSet name="Generic Import" source="Actual" freq="Day">')
        for st in stores.keys():
            fd.write('<Dimension ref_name="bu_code" value="' + st.__str__() + '">')
            fd.write('<Metric ref_name="Mercearia Itens">')
            for ds in stores[st]:
                d = ds[1]
                v = ds[2]
                fd.write('<Data date="{0}" value="{1:.2f}"/>'.format(d,v))
            fd.write('</Metric>')
            fd.write('</Dimension>')

        fd.write('</DataSet>')
        fd.write('</RadiantDocument>')
        conn.close()
        fd.close()
        fd = open(of+".flag", mode='w')
        fd.close()

'''
Export to XML file 15 minutes increment performed POS scans data
'''
def scans_exp(str_filter, date_filter, of):

    stmt = "select distinct storeid from daily_scans where " + str_filter + " " + date_filter
    conn = conn = psycopg2.connect(host=GPA_Config.pgsql_conn_str["host"], \
                            port=GPA_Config.pgsql_conn_str["port"], \
                            database=GPA_Config.pgsql_conn_str["database"], \
                            user=GPA_Config.pgsql_conn_str["user"], \
                            password=GPA_Config.pgsql_conn_str["password"])

    cur = conn.cursor()
    cur.execute(stmt)
    stores = cur.fetchall()

    if len(stores)>0:
        fd = open(of, mode='w', encoding='utf-8')
        fd.write(ROOT_EL)
        fd.write('<DataSet name="Generic Import" source="Actual" freq="QuarterHour">')

        stmt = "select to_char(date,'YYYY-MM-DDT') || to_char(time_incr, 'HH24:MI:SS') dt, scans " \
                "from daily_scans " \
                "where storeid = %s "
        if len(date_filter) > 0:
            stmt = stmt + date_filter
        #else:
        #    stmt = stmt + "and date like '" + year.__str__() + "%' "
        stmt += "order by dt"

        for store in stores:
            cur.execute(stmt, store)
            data = cur.fetchall()
            fd.write('<Dimension ref_name="bu_code" value="' + store[0].__str__() + '">')
            fd.write('<Metric ref_name="Lancamentos">')
            for d in data:
                fd.write('<Data date="{0}" value="{1:.2f}"/>'.format(d[0],d[1]))
            fd.write('</Metric>')
            fd.write('</Dimension>')
        fd.write('</DataSet>')
        fd.write('</RadiantDocument>')
        conn.close()
        fd.close()
        fd = open(of+".flag", mode='w')
        fd.close()

'''
Export to XML file 15 minutes increment amount of cash money receive in POS
'''
def dinheiro_exp(date_filter, of):
    stmt = "select distinct storeid from daily_cash where " + date_filter
    conn = conn = psycopg2.connect(host=GPA_Config.pgsql_conn_str["host"], \
                            port=GPA_Config.pgsql_conn_str["port"], \
                            database=GPA_Config.pgsql_conn_str["database"], \
                            user=GPA_Config.pgsql_conn_str["user"], \
                            password=GPA_Config.pgsql_conn_str["password"])

    cur = conn.cursor()
    cur.execute(stmt)
    stores = cur.fetchall()

    if len(stores)>0:
        fd = open(of, mode='w', encoding='utf-8')
        fd.write(ROOT_EL)
        fd.write('<DataSet name="Generic Import" source="Actual" freq="QuarterHour">')

        stmt = "select to_char(date,'YYYY-MM-DDT') || to_char(time_incr, 'HH24:MI:SS') dt, cash_amt " \
                "from daily_cash " \
                "where storeid = %s " \
                "and " + date_filter + " "\
                "order by dt"
        for store in stores:
            cur.execute(stmt, store)
            data = cur.fetchall()
            fd.write('<Dimension ref_name="bu_code" value="' + store[0].__str__() + '">')
            fd.write('<Metric ref_name="Dinheiro Vendas">')
            for d in data:
                fd.write('<Data date="{0}" value="{1:.2f}"/>'.format(d[0],d[1]))
            fd.write('</Metric>')
            fd.write('</Dimension>')
        fd.write('</DataSet>')
        fd.write ('</RadiantDocument>')
        conn.close()
        fd.close()
        fd = open(of+".flag", mode='w')
        fd.close()

'''
Export to XML file 15 minutes increment count of services tickets
'''
def services_exp(date_filter, of):
    stmt = "select distinct storeid from daily_services where " + date_filter
    conn = conn = psycopg2.connect(host=GPA_Config.pgsql_conn_str["host"], \
                            port=GPA_Config.pgsql_conn_str["port"], \
                            database=GPA_Config.pgsql_conn_str["database"], \
                            user=GPA_Config.pgsql_conn_str["user"], \
                            password=GPA_Config.pgsql_conn_str["password"])

    cur = conn.cursor()
    cur.execute(stmt)
    stores = cur.fetchall()

    if len(stores) > 0:
        fd = open(of, mode='w', encoding='utf-8')
        fd.write('<RadiantDocument CreationSource="GPA">')
        fd.write('<DataSet name="Generic Import" source="Actual" freq="QuarterHour">')

        stmt = "select to_char(date,'YYYY-MM-DDT') || to_char(time_incr, 'HH24:MI:SS') dt, count " \
                "from daily_services " \
                "where storeid = %s " \
                "and " + date_filter + " "\
                "order by dt"
        for store in stores:
            cur.execute(stmt, store)
            data = cur.fetchall()
            fd.write('<Dimension ref_name="bu_code" value="' + store[0].__str__() + '">')
            fd.write('<Metric ref_name="Servico">')
            for d in data:
                fd.write('<Data date="{0}" value="{1:.0f}"/>'.format(d[0],d[1]))
            fd.write('</Metric>')
            fd.write('</Dimension>')
        fd.write('</DataSet>')
        fd.write ('</RadiantDocument>')
        conn.close()
        fd.close()
        fd = open(of+".flag", mode='w')
        fd.close()

'''
Export to XML file 15 minutes increment counts of different transactions/actions
performed in POS
'''
def trxs_exp(date_filter, of):

    stmt = "select distinct storeid from daily_transactions where " + date_filter
    conn = conn = psycopg2.connect(host=GPA_Config.pgsql_conn_str["host"], \
                            port=GPA_Config.pgsql_conn_str["port"], \
                            database=GPA_Config.pgsql_conn_str["database"], \
                            user=GPA_Config.pgsql_conn_str["user"], \
                            password=GPA_Config.pgsql_conn_str["password"])

    cur = conn.cursor()
    cur.execute(stmt)
    stores = cur.fetchall()

    if len(stores)>0:
        fd = open(of, mode='w', encoding='utf-8')
        fd.write ('<?xml version="1.0" encoding="UTF-8"?>\n')
        fd.write ('<RadiantDocument CreationSource="WFM RedPrairie">\n')
        fd.write('<DataSet name="Generic Import" source="Actual" freq="QuarterHour">\n')

        stmt1 = "select distinct wfmr_name " \
                "from daily_transactions, gpa_to_wfmr_map " \
                "where storeid = %s " \
                "and gpa_name = trans_type "\
                "and " + date_filter

        stmt2 = "select to_char(date,'YYYY-MM-DDT') || to_char(increment, 'HH24:MI:SS') dt, count " \
                "from daily_transactions, gpa_to_wfmr_map " \
                "where storeid = %s " \
                "and " + date_filter + " " \
                "and wfmr_name = %s " \
                "and gpa_name = trans_type "\
                "order by dt"

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
        fd = open(of+".flag", mode='w')
        fd.close()

'''
Return different stores having sales
'''
def get_stores(filter):

    stmt = "select distinct storeid from daily_sales "

    conn = psycopg2.connect(host=GPA_Config.pgsql_conn_str["host"], \
                            port=GPA_Config.pgsql_conn_str["port"], \
                            database=GPA_Config.pgsql_conn_str["database"], \
                            user=GPA_Config.pgsql_conn_str["user"], \
                            password=GPA_Config.pgsql_conn_str["password"])
    cur = conn.cursor()
    if filter is not None:
        stmt = stmt + filter
    cur.execute(stmt)
    stores = cur.fetchall()
    conn.close()
    return stores


#Set precision to 2 digits
#getcontext().prec = 4
#Se the rounding rule
#getcontext().rounding = ROUND_UP
print("Starting metrics processing")
if len(argv)==1:
    exit()

#calc_mercearia(" date > '2015-08-01' and storeid = '1360' ")
#exit(1)
cmd = argv[1]
stime = datetime.datetime.now().time().isoformat()

if cmd == 'test':
    l_files = ('C:\\dev\\projects\\ScriptsUtil\\data\\GPA\\input\\WFMR_41201510.txt',)
    calculate_metrics(l_files)
elif cmd == 'proc':
    inpath = argv[2]
    #tmppath = argv[3]
    outpath = argv[3]
    elapsed = time()
    lto_proc = get_files(inpath)
    #ltmp_files = break_down_files   (inpath,tmppath)
    calculate_metrics(lto_proc, outpath)
    elapsed = time() - elapsed
    secs = elapsed%60
    mins = (elapsed-secs)/60

    print('Processing time:{0:.0f}:{1:.0f}(m:s)'.format(mins, secs))
elif cmd == 'exp_all': #export all metrics
    if len(argv) != 5:
        exit()
    #storeid = argv[2]
    path = argv[2]
    sdate = argv[3]
    edate = argv[4]

    stores = get_stores(None)
    #" where storeid in ('0076','0087','0608','1302','1307','1309','1319','1337',"\
    #                    "'1341','1350','1357','1359','1360','1377','1397','1669',"\
    #                    "'1686','1688','1707','1708','1710','1715','1877','2135','2430') ")

    for storeid in stores:
        sales_file = path + "\\GPA_sales_" + storeid[0].__str__() + ".xml"
        sales_exp("date between '" + sdate + "' and '" + edate + "' and storeid = '" + storeid[0].__str__() + "' ",sales_file)
        mercearia_file = path + "\\GPA_mercearia_" + storeid[0].__str__() + ".xml"
        mercearia_exp(" date between '" + sdate + "' and '" + edate + "' and storeid = '" + storeid[0].__str__() + "' ", mercearia_file)
        services_file = path + "\\GPA_services_" + storeid[0].__str__() + ".xml"
        services_exp(" date between '" + sdate + "' and '" + edate + "' and storeid = '" + storeid[0].__str__() + "' ", services_file)

        cash_file = path + "\\GPA_cash_" + storeid[0].__str__() + "_"
        items_file = path + "\\GPA_scans_" + storeid[0].__str__() + "_"
        trxs_file = path + "\\GPA_transactions_" + storeid[0].__str__() + "_"

        year_start = int(sdate[0:4])
        month_start = int(sdate[5:7])
        year_end = int(edate[0:4])
        month_end = int(edate[5:7])

        count = 1
        while (year_start < year_end or (year_start == year_end and month_start <= month_end )):
            m = month_start.__str__()
            if month_start < 10:
                m = '0' + m
            sdate2 = year_start.__str__() + '-' + m + '-01'

            month_start = month_start + 2
            if year_start == year_end and month_start > month_end:
                month_start = month_end
            if month_start > 12:
                month_start = 12
            m = month_start.__str__()
            if month_start < 10:
                m = '0' + m
            if month_start == 2:
                de = '28'
            elif month_start == 4 or month_start == 6 or month_start == 9 or month_start == 11:
                de = '30'
            elif month_start == 1 or month_start == 3 or month_start == 5 or month_start == 7 or month_start == 8 or month_start == 10 or month_start == 12:
                de = '31'
            edate2 = year_start.__str__() + '-' + m + '-' + de

            print("Exporting items between " + sdate2 + " and " + edate2 + " for store " + storeid[0].__str__())
            scans_exp(" storeid = '" + storeid[0].__str__() + "' ", " and date between '" + sdate2 + "' and '" + edate2 + "' ",items_file + count.__str__() + ".xml")
            print("Exporting transactions between " + sdate2 + " and " + edate2 + " for store " + storeid[0].__str__())
            trxs_exp(" date between '" + sdate2 + "' and '" + edate2 + "' and storeid = '" + storeid[0].__str__() + "' ", trxs_file + count.__str__() + ".xml")
            print("Exporting cash between " + sdate2 + " and " + edate2 + " for store " + storeid[0].__str__())
            dinheiro_exp("date between '" + sdate2 + "' and '" + edate2 + "' and storeid = '" + storeid[0].__str__() + "' ", cash_file + count.__str__() + ".xml")
            print("<-------------------------------------------------------------------------------->")
            count = count + 1
            if month_start == 12:
                year_start = year_start + 1
                month_start = 1
            else:
                month_start = month_start + 1
elif cmd == 'exp_mercearia':
    path = argv[2]
    sdate = argv[3]
    edate = argv[4]
    storeid = argv[5]
    mercearia_file = path + "\\GPA_mercearia_" + storeid[0].__str__() + ".xml"
    mercearia_exp(" date between '" + sdate + "' and '" + edate + "' and storeid = '" + storeid.__str__() + "' ", mercearia_file)
elif cmd == 'exp_services':
    path = argv[2]
    sdate = argv[3]
    edate = argv[4]
    stores = get_stores(None)
    for storeid in stores:
        services_file = path + "\\GPA_services_" + storeid[0].__str__() + ".xml"
        services_exp(" date between '" + sdate + "' and '" + edate + "' and storeid = '" + storeid[0].__str__() + "' ", services_file)
else:
    print("Don't know this command")

exit(1)
