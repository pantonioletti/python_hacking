#coding=UTF-8
#XXXXISO_8859-1
# -*- coding ISO_8859-1 -*-
'''
Created on Nov 30, 2009

@author: pantonio
'''

from sys import argv
from dbaccess.common import getConnection

if len(argv) < 2 or argv[1] == '?':
    print('Usage: ')
    print('python exec.py <params_file>')
    print('where params in params_file may be: ')
    print('    LOAD_ROT input_file db_target CPYTHON|JAVA')
    print('    ROTATIONS input_file db_target CPYTHON|JAVA')
    print('    ORG_GROUPS input_file db_target CPYTHON|JAVA')
    print('    ORG_POS input_file')
    print('    WRK_STDS input_file')
    print('    ORG_PARAM input_file db_target CPYTHON|JAVA')
    print('    FORCAST_PARAM input_file db_target CPYTHON|JAVA')
    print('    EQUATIONS input_file db_target CPYTHON|JAVA')
    print('    NEW_LINE input_file input_path output_path')
    print('    ORG_API input_file')
    print('    PRINT_EMP input_file input_xml_file output_path')
    print('    LOAD_ACT db_get input_file output_path db_target CPYTHON|JAVA')
    print('    FORECAST input_file')
    print('    STORE input_file')
    print('    VAL_ACT input_act_cds input_act_to_check')
    print('    REN_MAS input_file')

else:
    try:
        params = list()
        fd = open(argv[1], 'r')
        str = fd.readline()
        
        while(len(str) != 0):
            str = str.replace('\n', '')
            str = str.strip()
            if len(str) > 0 and str[0] != '#':
                params.append(str)
            str = fd.readline()
        fd.close()
    except IOError:
        print ("File ", argv[1], " not found")

    if len(params) > 0: 

        if params[0] == 'LOAD_ROT':
            from config.rotations import load_rotations3
            from wfm_db.load_data import get_activities
            from wfm_db.load_data import get_sched_plan
            
            conn = conn = getConnection(params[1], 'WFMFALA_CO')
            d_sp = get_sched_plan(conn)
            d_act = get_activities(conn)
            load_rotations3('C:/dev/projects/ScriptsUtil/data/input/fala_co_rotations.txt', d_sp, d_act)
            
        elif params[0] == 'ROTATIONS':
            from config.rotations import load_rotations
            from wfm_db.load_data import get_activities
            from wfm_db.load_data import get_sched_plan 
            
            conn = getConnection(params[1])
            d_act= get_activities(conn)
            d_sp = get_sched_plan(conn)
        #    conn.close()
            conn.begin()
            try:
                load_rotations('c:/dev/projects/ScriptsUtil/data/input/rotacionesCL2.txt',d_act, d_sp, conn)
            except:
                conn.rollback()
                raise
        
            #conn.rollback()
            conn.commit()
            conn.close()
            
            
        elif params[0] == 'ORG_GROUPS':
            from config.org_groups import load_attr12_db
            from config.org_groups import load_org_groups
            
            conn = getConnection(params[1])
            attr_12 = load_attr12_db(conn)
            conn.close()
            #load_attr_12('c:/dev/projects/ScriptsUtil/data/input/attr_12CL.txt')
            load_org_groups('c:/dev/projects/ScriptsUtil/data/input/org_groupsCL.txt', attr_12)    
        elif params[0] == 'ORG_POS':
            d_orgs = dict()
            from config.org_api import load_org_positions
            load_org_positions('C:/dev/projects/ScriptsUtil/data/input/falabella_co_org_positions.txt', d_orgs)    
        elif params[0] == 'WRK_STDS':
            #equations STEP 1
            from config.equations import work_stds
            work_stds('C:/dev/projects/ScriptsUtil/data/input/work_standardsCL.txt')
        
        elif params[0] == 'ORG_PARAM':
            
            from wfm_db.data_queries import get_org_groups
            from wfm_db.data_queries import get_uom
            from wfm_db.data_queries import get_org_entries
            from config.equations import insert_work_standards
        
            conn = getConnection(params[3], params[2])
            conn.begin()
            
            d_og = get_org_groups(conn)
            d_uom = get_uom(conn)
            d_oe = get_org_entries(conn)
            
            insert_work_standards(d_og, params[1], d_uom, conn, d_oe)
            #conn.rollback()
            conn.commit()
            conn.close()
        elif params[0] == 'FORCAST_PARAM':
            #equations STEP 2 Create forecast parameters
            from config.equations import load_var_el_grp
            from config.equations import insert_staff_vars
            from wfm_db.data_queries import get_forecast_def
            from wfm_db.data_queries import get_forecast_element
            from wfm_db.data_queries import get_forecast_groups
            
            conn = getConnection(params[3], params[2])
            conn.begin()
            d_def = get_forecast_def(conn)
            d_elem= get_forecast_element(conn)
            d_grp = get_forecast_groups(conn)
            elem_grp = load_var_el_grp(params[1], d_def, d_elem, d_grp)
            try:
                insert_staff_vars(elem_grp, conn)
            except:
                conn.rollback()
                raise
        
            #conn.rollback()
            conn.commit()
            conn.close()
        elif params[0] == 'EQUATIONS':
            #equations STEP 2 Create forecast parameters
            from config.equations import load_equations
            conn = getConnection(params[3], params[2])
            conn.begin()
            try:
                load_equations(params[1], conn)
            except:
                conn.rollback()
                raise
            #conn.rollback()
            conn.commit()
            conn.close()
        
        elif params[0] == 'NEW_LINE':
            import util.xml_misc
            
            param = list()
            task = 'NEW_LINE'
            if len(params) > 1:
                if len(params) != 5:
                    print("Call format:")
                    print("    pyhton exec.py NEW LINE <file name> <input path> <output path> <after this insert new line>")
                    exit()
                else:
                    param.append(params[1])
                    param.append(params[2])
                    param.append(params[3])
                    param.append(params[4])
            else:
                param.append('files.txt')
                param.append('C:/dev/projects/ScriptsUtil/data/input/')
                param.append('C:/dev/projects/ScriptsUtil/data/output/emp/')
                param.append('</entry>')
            util.xml_misc.start_task(task, param)
        elif params[0] == 'ORG_API':
            from config import org_api
            from config.org_api import load_positions
            from wfm_db.data_queries import get_activities
            
            conn = getConnection(params[6],params[5])
            
            d_act = get_activities(conn)
            conn.close()
            d_pos = load_positions(params[2],d_act, params[3])
            org_api.load_org_entries(params[1], params[3], params[4], d_pos)
        elif params[0] == 'LOAD_ACT':
            from config.activity_load import load_activities
        
            d_act = dict()    
            if params[1] == 'Y':
                from wfm_db.load_data import get_max_act_id
                from wfm_db.load_data import get_activities 
                
                conn = getConnection(params[1])
                d_act= get_activities(conn)
                max_id = get_max_act_id(conn)
            else:
                d_act = {1:'Test', 74:'INDIVACC', 75:'MR'}
                max_id = 75
            max_id += 1
            
            load_activities(params[2], params[3], max_id, d_act)    
        elif params[0] == 'FORECAST':
            from config.forecast import load_forecast
            from config.forecast import print_forecast_body
            
            data = load_forecast(params[1])
            #assign_ids(data)
            print('<?xml version="1.0" encoding="ISO_8859-1"?>')
            print('<!DOCTYPE root SYSTEM "Forecast.dtd">')
            print('<root>')
            print_forecast_body(data[0], data[1], data[2])
            #orgs = attr12_org_structure("c:/dev/projects/pwmpython/BOrgStructure.txt", data[2])
            #uuid = 1
            #uuid = definitions(data, uuid)
            #elems_and_groups(data, uuid)
            print('</root>')
        elif params[0] == 'STORE':
            from config.store_structure import load_orgs
            
            load_orgs("c:/dev/projects/scriptsutil/data/input/org_entries_ripleyCL.txt")
        elif params[0] == 'VAL_ACT':
            from wfm_db.data_validation import act_wo_position
            act_wo_position('C:/dev/projects/ScriptsUtil/data/input/activity_codesCL.txt','C:/dev/projects/ScriptsUtil/data/input/act_sin_posCL.txt')
        elif params[0] == 'REN_MAS':
            from util.xml_misc import rename_massive
            
            rename_massive(params[1])
        elif params[0] == 'EXCEL':
            from wfm_db.load_config import getExcelData
            from wfm_db.load_config import load_entreprise_model
            load_entreprise_model('C:/dev/projects/WFM/FormatoExcel.txt') 
            #getExcelData('C:\\dev\\projects\\WFM\\1 EnterpriseModelConfiguration (v.20100514).xlsx')
        else:
            print("Something wrong with yours parameters try with ?")
