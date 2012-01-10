#coding=ISO_8859-1
'''
Created on Feb 26, 2010

@author: pantonio
'''
import cx_Oracle
from wfm_db import rotations

#tables = remove_org.load_tables('C:/dev/projects/ScriptsUtil/data/input/org_tables.txt')
#remove_org.run_select(tables)
#orgs = remove_org.get_all_dep_orgs(1434)
#remove_org.remove_org_list(orgs)
conn = cx_Oracle.connect('ewmuser','ewmuser','wfm_ripley_pe_jda')
#orgs = rotations.start_process('COMPARE_POSITIONS', [1430, 21], conn )#[1430, 21])
rot = rotations.start_process('EMP_W_OUT_ROTATION', ['20100405', '20100411'], conn )
for rot_id in rot[3].keys():
    str = "Código empleado: " + rot[3][rot_id][5] + "\n"
    str += "Apellidos : " + rot[3][rot_id][6] + "\n"
    str += "Nombres : " + rot[3][rot_id][7] + "\n"
    str += "Fecha estado: " + rot[3][rot_id][12]+ "\n"
    org = rot[1][rot[3][rot_id][3]]
    str += "Organización: " + org.cd + " " + org.name + "\n"
    str += "Posición: " + rot[3][rot_id][8] + " " + rot[3][rot_id][9] + " Fecha:" + rot[3][rot_id][13] + "\n"
    str += "Plan de horario: " + rot[3][rot_id][10] + " " + rot[3][rot_id][11] + " Fecha:" + rot[3][rot_id][14] + "\n"
    print(str)
    
#0: esp.emp_id, 
#1:esp.sched_plan_id, 
#2:op.org_position_id, 
#3:op.org_entry_id,
#4:rot_id
#5:e.hr_emp_id, 
#6:e.last_name, 
#7:e.first_name, 
#8:op.org_position_cd, 
#9:op.org_position_name, 
#10:sp.sched_plan_cd, 
#11:sp.sched_plan_name
#12: emp status date
#13: pos date
#14: sched plan date

conn.close()
