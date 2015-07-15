# -*- coding: utf-8 -*-
__author__ = 'pantonio'

exec_cmd = 'calc_mercearia' #'file_import'|'sales'|'items'|'trx_det'|'trx_tot'|'mercearia'|'cash'|'count_trxs'|'calc_sales'
#                        'calc_items'|'calc_mercearia'
out_file = 'C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\Data\\intrefaces\\GPA_daily_trxs_det_20150715.xml'
sqlite_db=''
'''
'C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\Data\\input\\vendas_2013_0608.tab',
            'C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\Data\\input\\vendas_2014_0608.tab',
            'C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\Data\\input\\vendas_EP_19052015a06062015.tab',
            'C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\Data\\input\\vendas_2013_EP.tab',
            'C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\Data\\input\\vendas_2014_EP.tab',
            'C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\Data\\input\\vendas_EX_19052015a06062015.txt',
            'C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\Data\\input\\vendas_2013_EX.tab',
            'C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\Data\\input\\vendas_2015_EP.tab',
            'C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\Data\\input\\vendas_2014.tab',
            'C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\Data\\input\\vendas_2015_EX.tab',
'''
files2proc=('C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\Data\\input\\vendas_EX_28062015a05072015.tab',)

DB_FILE = "C:\\Users\\pantonio\\Documents\\JDA\\WFM\\GPA\\DATA\\gpa_db.db"
#mysql_conn_str={'user':'root','password':'odd6lamp','host':'localhost','database':'gpa_interfaces'}
mysql_conn_str={'user':'root','password':'odd6lamp','host':'localhost','port':'3307','database':'gpa_interfaces'}
replacements={'\n':'',',':'.','DINHEIRO':'Transacao Dinheiro','CREDITO - DEBITO':'Transacao Cartão','CHEQUE':'Transacao Cheque','RECOMPENSAS':'Transacao Dinheiro'}
