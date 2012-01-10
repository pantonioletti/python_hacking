'''
Created on Feb 26, 2010

@author: pantonio
'''
from dbaccess import OracleDBAccess

def remove_org(org_id):
    #Tienda
    odba = OracleDBAccess.OracleDBAccess('ewmuser','ewmuser','wfm_ripley_pe_stg')
    odba.begin()
    try:
        print('Removing org_id: ' + org_id.__str__() )
        sql = 'delete from forecast_data fd where fd.org_entry_id = '  + org_id.__str__()
        odba.executeQuery(sql)
        print('.')
        sql = 'delete from org_hours_pattern ohp where ohp.org_entry_id = '  + org_id.__str__()
        odba.executeQuery(sql)
        print('.')
        sql = 'delete from budget_actual_value bav where bav.org_entry_id = '  + org_id.__str__() + ' or bav.budget_id in (select b.budget_id from budget b where b.org_entry_id = '  + org_id.__str__() + ')'
        odba.executeQuery(sql)
        print('.')
        sql = 'delete from budget b where b.org_entry_id = '  + org_id.__str__()
        odba.executeQuery(sql)
        print('.')
        #DP
        sql = 'delete from org_group_org_entry ogoe where ogoe.org_entry_id = '  + org_id.__str__()
        odba.executeQuery(sql)
        print('.')
        sql = 'delete from budget_detail_import bdi where bdi.org_entry_id = '  + org_id.__str__()
        odba.executeQuery(sql)
        print('.')
        
        #UE
        sql = 'delete from budget_org_to_org boto where boto.org_entry_id = '  + org_id.__str__() + ' or boto.parent_org_entry_id = '  + org_id.__str__() + ' or boto.budget_level_org_entry_id = '  + org_id.__str__()
        odba.executeQuery(sql)
        print('.')
        sql = 'delete from org_position_activity opa where opa.org_position_id in (select org_position_id from org_position op where op.org_entry_id = '  + org_id.__str__() + ')'
        odba.executeQuery(sql)
        print('.')
        sql = 'delete from org_position_status ops where ops.org_position_id in (select org_position_id from org_position op where op.org_entry_id = '  + org_id.__str__() + ')'
        odba.executeQuery(sql)
        print('.')
        sql = 'delete from org_position op where op.org_entry_id = '  + org_id.__str__()
        odba.executeQuery(sql)
        print('.')
        sql = 'delete from org_relation ore where ore.parent_org_id = '  + org_id.__str__() + ' or ore.child_org_id = '  + org_id.__str__()
        odba.executeQuery(sql)
        print('.')
        sql = 'delete from org_sched_rotation osr where osr.org_entry_id = '  + org_id.__str__()
        odba.executeQuery(sql)
        sql = 'delete from org_attribute_value oav where oav.org_entry_id = '  + org_id.__str__()
        print('.')
        odba.executeQuery(sql)
        sql = 'delete from org_status os where os.org_entry_id = '  + org_id.__str__()
        print('.')
        odba.executeQuery(sql)
        sql = 'delete from org_entry oe where oe.org_entry_id = '  + org_id.__str__()
        odba.executeQuery(sql)
        print('.')
        odba.commit()
        print('Done!\n')
    except (Exception):
        print(Exception.message)
    odba.close()

def remove_org_list(org_list):
    org_it = iter(org_list)
    for org_id in org_it:
        remove_org(org_id)
    
def get_all_dep_orgs(org_id):
    odba = OracleDBAccess.OracleDBAccess('ewmuser','ewmuser','wfm_ripley_pe_stg')
    sql = 'select child_org_id from org_relation where parent_org_id = ' + org_id.__str__()
    rows_it = odba.executeQuery(sql)
    orgs = list()
    orgs.append(org_id)
    row = rows_it.next()
    while(row is not None):
        orgs.append(row[0])
        row = rows_it.next()
    odba.close()
    return orgs
    
    
    
def load_tables(file):
    fd = open(file,'r')
    str = fd.readline()
    tables = list()
    while(len(str) != 0):
        str = str.replace('\n', '')
        tables.append(str)
        str = fd.readline()
    return(tables)

def run_select(tables):
    #odba = OracleDBAccess.OracleDBAccess('ewmuser','ewmuser','wfm_ripley_pe_stg')
    if (len(tables) > 0):
        tab_it = iter(tables)
        for tab in tab_it:
            sql = 'select * from ' + tab + '\n'
            print(sql)
            #rows = odba.executeQuery(sql)
            #one_row = rows.next()
            #while(one_row is not None):
            #    print(one_row)
            
    