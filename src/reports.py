'''
Created on Dec 22, 2010

@author: pantonio
'''
from sys import argv
from dbaccess.common import getConnection

if len(argv) < 2 or argv[1] == '?':
#if argv[1] == '?':
    print('Usage: ')
    print('python exec.py <params_file>')
    print('where params in params_file may be: ')
    print('    REPROT start_date end_date db_target CPYTHON|JAVA')
    print('    ROTBAL db_target CPYTHON|JAVA')
    print('    MULTIW start_date end_date db_target CPYTHON|JAVA')
    print('    EMP_ROT start_date end_date db_target CPYTHON|JAVA')

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

    if len(params > 0): 

        if params[0] == 'REPROT':
            from wfm_db.rotations_rebuild import get_emps_to_fix
            #from wfm_db.rotations_rebuild import get_constraint_dom
            
            #xml = "<c1><dbe><d>2</d><b>0000</b><e>0000</e></dbe><dbe><d>3</d><b>0000</b><e>0000</e></dbe><dbe><d>4</d><b>0000</b><e>0000</e></dbe><dbe><d>7</d><b>0000</b><e>0000</e></dbe><dbe><d>1</d><b>0000</b><e>0000</e></dbe></c1>"
            #constraint = get_constraint_dom(xml)
            #exit()
            conn = getConnection(params[4], params[3])
        
            emps_to_fix = get_emps_to_fix(conn, params[1], params[2])
            print("Got " + len(emps_to_fix).__str__() + " employees to fix")
        elif params[0] == 'ROTBAL':
            from wfm_db.rotations_rebuild import get_better
            conn = getConnection(params[1], params[2])
        
            get_better(conn)
            
        elif params[0] == 'MULTIW':
            from reports.multiweek import emp_multiweek_rep
            conn = getConnection(params[3])
        
            emps = emp_multiweek_rep(params[1], params[2], conn)
            conn.close()
            for e in emps.keys():
                emps[e].pprint()
                
        elif params[0] == 'EMP_ROT':
            conn = getConnection(params[1])
            from wfm_db import rotations
        
            #orgs = rotations.start_process('COMPARE_POSITIONS', [1430, 21], conn )#[1430, 21])
            rot = rotations.start_process('EMP_W_OUT_ROTATION', [params[2], params[3]], conn )
            for rot_id in rot[3].keys():
                str = "Codigo empleado: " + rot[3][rot_id][5] + "\n"
                str += "Apellidos : " + rot[3][rot_id][6] + "\n"
                str += "Nombres : " + rot[3][rot_id][7] + "\n"
                str += "Fecha estado: " + rot[3][rot_id][12]+ "\n"
                org = rot[1][rot[3][rot_id][3]]
                str += "Organizacion: " + org.cd + " " + org.name + "\n"
                str += "Posicion: " + rot[3][rot_id][8] + " " + rot[3][rot_id][9] + " Fecha:" + rot[3][rot_id][13] + "\n"
                str += "Plan de horario: " + rot[3][rot_id][10] + " " + rot[3][rot_id][11] + " Fecha:" + rot[3][rot_id][14] + "\n"
                print(str)
            conn.close()
        elif params[0] == 'PRINT_EMP':
            import util.xml_misc
            
            param = list()
            task = 'PRINT_EMP'
            param.append('C:/dev/projects/ScriptsUtil/data/input/sin_rotacion.txt')
            param.append('C:/temp/ripley/emp/nl/PEEMPLEADOS_20100330-232938-474.xml')
            param.append('C:/dev/projects/ScriptsUtil/data/output/')
            util.xml_misc.start_task(task, param)
        else:
            print("Something wrong with yours parameters try with ?")
