import os
from io import StringIO
from reports import PWMRepCommon
#from  java.io import PrintWriter
#from  java.io import FileOutputStream
#from os import fdopen
import sys
#import cx_Oracle

def empWithoutRot(connStr, start_sdate, end_sdate, org_cd, output):
    # Paso 1 : obtener todos los sub orgs
    #conn = PWMRepCommon.openConnJDBC(connStr)
    conn = PWMRepCommon.openConn(connStr)
    orgs = PWMRepCommon.getAllChildrenConn(conn, org_cd)
    if (len(orgs) == 0):
        conn.close()
        return None
    to_print = list()
    # Paso 2 : por cada sub org obtener rotaciones
    for i in range(0, len(orgs)):
        rots = PWMRepCommon.getRotations(conn, orgs[i].id,start_sdate, end_sdate)
        if (rots is None):
            continue
        already_print = False
        # Paso 3: si hay rotacion obtener las posiciones
        poss = PWMRepCommon.getActivePositions(conn, orgs[i].id, start_sdate, end_sdate)
        if (poss is None):
            continue
        # Paso 4: si hay posiciones obtener los empleados
        emps = list()
        for j in range(0, len(poss)):
            tmp_list = PWMRepCommon.getActiveEmpPos(conn, poss[j], start_sdate, end_sdate)
            if (tmp_list is not None):
                emps.extend(tmp_list)
            #print "    Position : ",  poss[j].code, " ", poss[j].name
        if (len(emps)== 0):
            continue
        # Paso 5: para cada empleado obtener su plan de horarios
        for j in range(0, len(emps)):
            PWMRepCommon.setSchedPlans(conn, emps[j], start_sdate, end_sdate)
        
        # Paso 6: Verificar para cada empleados rotaciones para las que califica
        for j in range(0, len(emps)):
            employee = emps[j]
            for k in range(0, len(rots)):
                rotation = rots[k]
                apply = False
                for l in range(0, len(rotation.sched_plans)):
                    if (rotation.sched_plans[l][0] in employee.sched_plans):
                        apply = True
                        break
                if (apply):
                    empAct = employee.getActivities()
                    for l in range(0, len(rotation.activities)):
                        if (not (rotation.activities[l][0] in empAct)):
                            apply = False
                            break
                if (apply):
                    employee.addQualifyingRot(rotation)
            if (len(employee.qual_rot) > 0):
                rot_list = PWMRepCommon.getAppliedRot(conn, employee.id, start_sdate, end_sdate)
                if (len(rot_list)==0):
                    if (not already_print):
                        to_print.append(orgs[i])
                        print ("ORG : ", orgs[i].code, "   ", orgs[i].name)
                        already_print = True
                    employee.setNoRotation()
                    to_print.append(employee)
                    employee.printEmployee()
                    print ("Employee without rotation")
                    print ("")
                    print ("")
                else:
                    has_qual_rot = False
                    for l in range(0, len(rot_list)):
                        if (rot_list[l][0] in employee.qual_rot):
                            has_qual_rot = True
                            break
                    if (not has_qual_rot):
                        if (not already_print):
                            to_print.append(orgs[i])
                            print ("ORG : ", orgs[i].code, "   ", orgs[i].name)
                            already_print = True
                        employee.setAppliedRot(rot_list)
                        to_print.append(employee)
                        employee.printEmployee()
                        print ("Has these rotations:", rot_list)
                        print ("")
                        print ("")
    conn.close()
    #fd = FileOutputStream(output)
    #writer = PrintWriter(fd)
    
    fd = open(output, 'a')
    for i in range(0, len(to_print)):
        fd.write(to_print[i].print_me())
        fd.write('\n')
    fd.close()
    return None

def multiRotEmployees(connStr, start_sdate, end_sdate, org_cd, output):
    # Paso 1 : obtener todos los sub orgs
    #conn = PWMRepCommon.openConnJDBC(connStr)
    conn = PWMRepCommon.openConn(connStr)
    orgs = PWMRepCommon.getAllChildrenConn(conn, org_cd)
    if (len(orgs) == 0):
        conn.close()
        return None
    to_print = list()
    # por cada sub org 
    multi_rot_emp = list()
    for i in range(0, len(orgs)):
        # Paso 2 : obtener rotaciones
        rots = PWMRepCommon.getRotations(conn, orgs[i].id,start_sdate, end_sdate)
        if (rots is None):
            continue
        already_print = False
        # Paso 3: si hay rotacion obtener las posiciones
        poss = PWMRepCommon.getActivePositions(conn, orgs[i].id, start_sdate, end_sdate)
        if (poss is None):
            continue
        # Paso 4: si hay posiciones obtener los empleados
        emps = list()
        for j in range(0, len(poss)):
            tmp_list = PWMRepCommon.getActiveEmpPos(conn, poss[j], start_sdate, end_sdate)
            if (tmp_list is not None):
                emps.extend(tmp_list)
        if (len(emps)== 0):
            continue
        # Paso 5: obtener posiciones asociadas a empleados
        rot_list = ""
        if (len(rots) > 0):
            l = len(rots)
            for j in range(0, l):
                rot_list = rot_list + rots[j].id.__str__()
                if (j < l-1):
                    rot_list = rot_list + ","
        emp_list = ""
        emp_data = dict()
        
        # Si hay rotatciones buscamos empleados
        if (len(rots) > 0):
            l = len(emps)
            for j in range(0, l):
                emp_list = emp_list + emps[j].id.__str__()
                emp_data[emps[j].id] = emps[j]
                if (j < l-1):
                    emp_list = emp_list + ","
        emp_rot = PWMRepCommon.getEmpRotations(conn, rot_list, emp_list, start_sdate, end_sdate)
        last_added = None
        temp = None
        for j in range(1, len(emp_rot)):
            if (emp_rot[j][0] == emp_rot[j-1][0]):
                if (last_added is None or last_added != emp_rot[j][0]):
                    if (temp is not None):
                        multi_rot_emp.append(temp)
                    employee = emp_data[emp_rot[j][0]]
                    temp = [[orgs[i].code, orgs[i].name],[employee.hr_id, employee.last, employee.first],
                            [emp_rot[j-1][2], emp_rot[j-1][3], str(emp_rot[j][4]), str(emp_rot[j-1][5])]]
                temp.append([emp_rot[j][2], emp_rot[j][3], str(emp_rot[j][4]), str(emp_rot[j][5])])
                last_added = emp_rot[j][0]
        if (temp is not None):
            multi_rot_emp.append(temp)

    conn.close()
            
    fd = open(output, 'a')
    sfd = StringIO.StringIO()
    for i in range(0, len(multi_rot_emp)):
        #print str(multi_rot_emp[i]) >> fd
        sfd.write(multi_rot_emp[i])
        sfd.write('\n')
    print (sfd.getvalue())
    fd.write(sfd.getvalue())
    sfd.close()
    fd.close()
    
    return None
    
def compOrgPosition(connStr, start_sdate, end_sdate, org_cd, org_mod, output):
    conn = PWMRepCommon.openConn(connStr)
    orgs = PWMRepCommon.getAllChildrenConn(conn, org_mod)
    if (len(orgs) == 0):
        conn.close()
        return None
    for i in range(0, len(orgs)):
        # Paso 4: si hay posiciones obtener los empleados
        orgs[i].setAttr12(PWMRepCommon.getOrgAttr(conn, orgs[i].id, 12))

    orgs_c = PWMRepCommon.getAllChildrenConn(conn, org_cd)
    if (len(orgs_c) == 0):
        conn.close()
        return None
    to_comp_12 = dict()
    for i in range(0, len(orgs_c)):
        # Paso 4: si hay posiciones obtener los empleados
        orgs_c[i].setAttr12(PWMRepCommon.getOrgAttr(conn, orgs_c[i].id, 12))
        if (orgs_c[i].attr12 is not None):
            to_comp_12[orgs_c[i].attr12] = orgs_c[i]
        
    to_print = list()
    # Paso 2 : por cada sub org obtener rotaciones
    for i in range(0, len(orgs)):
        poss = PWMRepCommon.getActivePositions(conn, orgs[i].id, start_sdate, end_sdate)
        if (poss is None):
            continue
        # Paso 4: si hay posiciones obtener los empleados
        for j in range(0, len(poss)):
            comp_org = to_comp_12[orgs[i].attr12]
            if (comp_org is None):
                continue
            
            if (not PWMRepCommon.valOrgPos(conn, comp_org.id, 12, comp_org.attr12, poss[j].code, start_sdate, end_sdate)):
                print ("Depto: ", comp_org.attr12, "  ", poss[j].print_me()) 
                