# -*- coding: utf-8 -*-
__author__ = 'pantonio'

mssql_conn_str={'user':'sa','password':'MicrosoftSucks@01','host':'J1006568WIN7LT\SQLEXPRESS','database':'GPA_TRXS'}
exec_cmd = 'exp_all' #'file_import'|'sales'|'items'|'trx_det'|'trx_tot'|'mercearia'|'cash'|'count_trxs'|'calc_sales'
#                        'calc_items'|'calc_mercearia'|'calc_cash'|'calc_all'|'exp_all'
out_file = 'C:\\dev\\projects\\ScriptsUtil\\data\\GPA\\output\\GPA_mercearia_1350_2014_2015.xml'
#'C:\\dev\\projects\\ScriptsUtil\\data\\GPA\\output\\GPA_daily_trxs_det_1337_JulAug_2015.xml'
out_sales = ('C:\\dev\\projects\\ScriptsUtil\\data\\GPA\\output\\GPA_daily_sales_1669_2015_3.xml',)
out_items = ('C:\\dev\\projects\\ScriptsUtil\\data\\GPA\\output\\GPA_daily_items_1669_2015_3.xml',)
out_trxs = ('C:\\dev\\projects\\ScriptsUtil\\data\\GPA\\output\\GPA_daily_trxs_det_1669_2015_3.xml',)
out_cash = ('C:\\dev\\projects\\ScriptsUtil\\data\\GPA\\output\\GPA_daily_cash_1669_2015_3.xml',)

sqlite_db=''
'''
'C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\Data\\input\\vendas_2013_0608.tab',
'''
files2proc=('C:\\dev\\projects\\ScriptsUtil\\data\\GPA\\input\\WFMR_25_lojas_1669.txt',)
# \
#             'C:\\dev\\projects\\ScriptsUtil\\data\\GPA\\input\\GPA_0608_2.txt',\

#'C:\\dev\\projects\\ScriptsUtil\\data\\GPA\\input\\GPA_1350.txt','C:\\dev\\projects\\ScriptsUtil\\data\\GPA\\input\\GPA_1350_2.txt',)

DB_FILE = "C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\DATA\\gpa_db.db"
#mysql_conn_str={'user':'root','password':'odd6lamp','host':'localhost','database':'gpa_interfaces'}
mysql_conn_str={'user':'root','password':'odd6lamp','host':'localhost','port':'3307','database':'gpa_interfaces'}
replacements={'\n':'',',':'.','DINHEIRO':'Transacao Dinheiro','CREDITO - DEBITO':'Transacao Cartao','CHEQUE':'Transacao Cheque','RECOMPENSAS':'Transacao Dinheiro'}
