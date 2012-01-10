#coding=ISO_8859-1
'''
Created on Mar 1, 2010

@author: pantonio
'''
#from sched_classes import Emp
from wfm_db.sched_classes import Rotation
from wfm_db.sched_classes import Org

def get_orgs_for_rot(start_date, end_date, rot_id, conn):
    
    sql = "select osr.org_entry_id, oe.org_entry_cd, oe.org_entry_name "
    sql += "from org_sched_rotation osr, org_entry oe "
    sql += "where osr.sched_rotation_id = " + rot_id.__str__() + " "
    sql += "and osr.eff_sdate <= '" + end_date + "' "
    sql += "and (osr.end_sdate > '" + start_date + "' or osr.end_sdate is null) "
    sql += "and osr.org_entry_id = oe.org_entry_id"
    
    orgs = None
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    if (len(data) > 0):
        orgs = data
        
    return orgs
    

def get_all_rotations(start_date, end_date, conn):
    sql = "select sr.sched_rotation_id, sr.sched_rotation_cd, sr.sched_rotation_name, sr.sched_rotation_type_id, "
    sql += "srsp.sched_plan_id, sra.activity_entry_id "
    sql += "from sched_rotation sr, sched_rotation_sched_plan srsp, sched_rotation_activity sra "
    sql += "where sr.sched_rotation_id = srsp.sched_rotation_id "
    sql += "and sr.sched_rotation_id = sra.sched_rotation_id (+) "

    cursor = conn.cursor()
    rotations = dict()
    orgs = dict()
    
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    if (len(data) > 0):
        for next_rot in data:
            if (next_rot[0] not in rotations):
                new_rot = Rotation(next_rot[0], next_rot[1], next_rot[2], next_rot[3])
                rotations[next_rot[0]] = new_rot
            else:
                new_rot = rotations[next_rot[0]]
            new_rot.add_sched_plan(next_rot[4])
            if (new_rot.type == 2 and next_rot[5] is not None):
                new_rot.add_activity(next_rot[5])
    for next_rot in rotations.keys():
        org_rot = get_orgs_for_rot(start_date, end_date, next_rot, conn)
        if org_rot is not None:
            for org_item in org_rot:
                rotations[next_rot].add_org(org_item[0])
                if org_item[0] not in orgs:
                    orgs[org_item[0]] = Org(org_item[0], org_item[1], org_item[2])
    return [rotations, orgs]

def get_pos_act_filter(start_date, end_date, rot, conn):
    
    filter = ""
    count = 0
    if len(rot.orgs)== 0:
        filter = None
    else:
        sql = "select opa.org_position_id, count(*) "
        sql += "from org_position_activity opa, org_position op, org_position_status ops "
        sql += "where opa.activity_entry_id in ("
        for act_id in rot.activities:
            count += 1
            sql += act_id.__str__() + ","
        sql = sql.rstrip(',')
        sql += ") "
        sql += "and opa.eff_date <= to_date('" + end_date + "', 'yyyymmdd') "
        sql += "and (opa.end_date > to_date('" + start_date + "', 'yyyymmdd') or ops.end_date is null) "
        sql += "and ops.eff_date <= to_date('" + end_date + "', 'yyyymmdd') "
        sql += "and (ops.end_date > to_date('" + start_date + "', 'yyyymmdd') or ops.end_date is null) "
        sql += "and op.org_entry_id in ("
        for org_id in rot.orgs:
            count += 1
            sql += org_id.__str__() + ","
        sql = sql.rstrip(',')
        sql += ") "
        sql += "and ops.org_position_id = opa.org_position_id "
        sql += "and op.org_position_id = opa.org_position_id "
        sql += "group by opa.org_position_id "
        sql += "having count(*) = " + count.__str__()
        
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
        except:
            print(sql)
            raise
        data = cursor.fetchall()
        cursor.close()
        
        if len(data) > 0:
            filter = "("
            for pos_item in data:
                filter += pos_item[0].__str__() + ","
            filter = filter.rstrip(',')
            filter += ") "
        else:
            filter = None
        
    return filter 
        
def get_quali_emp_for_rot(start_date, end_date, drot, dorg, conn):
    
    demp = dict()
    
    for rot_id in drot.keys():
        rot = drot[rot_id]
        sql = "select esp.emp_id, esp.sched_plan_id, op.org_position_id, op.org_entry_id, " + rot_id.__str__() + ", "
        sql += "e.hr_emp_id, e.last_name, e.first_name, op.org_position_cd, op.org_position_name, sp.sched_plan_cd, sp.sched_plan_name, "
        sql += "to_char(es.eff_date,'yyyymmdd'), to_char(eop.eff_date,'yyyymmdd'), esp.eff_sdate "
        sql += "from org_position op, emp_org_position eop, emp_sched_plan esp, org_position_status ops, emp_status es, emp e, sched_plan sp "
        sql += "where ops.status_id = 1 "
        sql += "and e.emp_id = esp.emp_id "
        sql += "and esp.sched_plan_id = sp.sched_plan_id "
        
        if rot.type == 2:
            filter = get_pos_act_filter(start_date, end_date, rot, conn)
            if filter == None:
                continue
            sql += "and op.org_position_id in "
            sql += filter
        else:
            if len(rot.orgs) > 0:
                sql += "and op.org_entry_id in ("
                for org_id in rot.orgs:
                    sql += org_id.__str__() + ","
                sql = sql.rstrip(',')
                sql += ") "
            else:
                continue

        if len(rot.sched_plan) > 0:
            sql += "and esp.sched_plan_id in ("
            for sp_id in rot.sched_plan:
                sql += sp_id.__str__() + ","
            sql = sql.rstrip(',')
            sql += ") "
        else:
            return None

        sql += "and ops.eff_date <= to_date('" + end_date + "','yyyymmdd') "
        sql += "and (ops.end_date > to_date('" + start_date + "','yyyymmdd') or ops.end_date is null) "
        sql += "and es.eff_date <= to_date('" + end_date + "','yyyymmdd') "
        sql += "and (es.end_date > to_date('" + start_date + "','yyyymmdd') or es.end_date is null) "
        sql += "and esp.eff_sdate <= '" + end_date + "' "
        sql += "and (esp.end_sdate > '" + start_date + "' or esp.end_sdate is null) "
        
        sql += "and eop.org_position_id = op.org_position_id "
        sql += "and esp.emp_id = eop.emp_id "
        sql += "and es.emp_id = eop.emp_id "
        sql += "and ops.org_position_id = op.org_position_id "

        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        if (len(data) > 0):
            for next_emp in data:
                demp[next_emp[0]] = next_emp
    return demp

def get_emp_w_out_rot(start_date, end_date, quali_emps, conn):
    
    demp = dict()
    
    for emp_id in quali_emps.keys():
        sql = "select count(*) "
        sql += "from emp_sched_rotation esr "
        sql += "where esr.eff_sdate <= '" + start_date + "' "
        sql += "and (esr.end_sdate > '" + end_date + "' or esr.end_sdate is null) "
        sql += "and esr.sched_rotation_id = " + quali_emps[emp_id][4].__str__() + " "
        sql += "and esr.emp_id = " + emp_id.__str__() + " "

        cursor = conn.cursor()
        cursor.execute(sql)
        data = cursor.fetchone()
        if (data[0] == 0):
            demp[emp_id] = quali_emps[emp_id]
    cursor.close()
    return demp

def start_process(action, param, conn):
    
    if action == 'COMPARE_POSITIONS':
        compare_org_positions(param[0], param[1], conn)
        data = None
    elif action == 'EMP_W_OUT_ROTATION':
        data = get_all_rotations(param[0], param[1], conn)
        emps = get_quali_emp_for_rot(param[0], param[1], data[0], [1], conn)
        data.append(emps)
        emps_wo_rot = get_emp_w_out_rot(param[0], param[1], emps, conn)
        data.append(emps_wo_rot)
        #quali_emps = get_emp_pos_sched_plan(param[0], param[1], conn) 
    else:
        data = get_sub_orgs(param, conn)
        data.append(param)
        all_pos = dict()
        for org_id in data:
            get_org_pos(org_id, all_pos, conn)
    
        for org_id in all_pos.keys():
            for pos in all_pos[org_id]:
                count = count_pos_activities(pos[0], conn)
                if count == 1:
                    print(pos)
        
    return data

def compare_org_positions(org_id1, org_id2, conn):
    data1 = dict()
    build_dict_by_org_cd(data1, org_id1, conn)
    data2 = dict()
    build_dict_by_org_cd(data2, org_id2, conn)

    keys = data1.keys()
    for key in keys:
        if key not in data2:
            print('Org ' + data1[key][1] + ' ' + data1[key][2] + ' does not exist in ' + org_id2.__str__())
            continue
        positions1 = get_org_pos(data1[key][0], conn)
        positions2 = get_org_pos(data2[key][0], conn)
        bad_data = 0
        for pos_k in positions1.keys():
            if (pos_k not in positions2):
                print('Position ' + pos_k + ' - "' + positions1[pos_k][2] + '" not found at org ' + data2[key][4] + ' but present at' + data1[key][4])
                bad_data += 1
            count1 = count_pos_activities(positions1[pos_k][0], conn)
            count2 = count_pos_activities(positions2[pos_k][0], conn)
            if count1 != count2:
                print('Position ' + pos_k + ' - "' + positions1[pos_k][2] + '" at org ' + data2[key][4] + ' has : ' + count1.__str__() + ' activities but at org ' + data1[key][4] + ' has ' + count2.__str__() + ' activities')
        if bad_data > 0 or len(positions1) != len(positions2):
            for pos_k in positions2.keys():
                if (pos_k not in positions1):
                    print('Position ' + pos_k + ' - "' + positions2[pos_k][2] + '" not found at org ' + data1[key][4] + ' but present at' + data2[key][4])
    return
    
def build_dict_by_org_cd(org_dict, org_id, conn):

    sql = 'select oe.org_entry_id, substr(oe.org_entry_cd,3,2), '
    sql += 'substr(oe.org_entry_cd,length(oe.org_entry_cd)-3), oe.org_entry_name, oe.org_entry_cd '
    sql += 'from org_relation  ore, org_entry oe '
    sql += 'where parent_org_id = ' + org_id.__str__() + ' '
    sql +=  'and oe.org_entry_id = ore.child_org_id'
    
    cursor = conn.cursor()
    
    cursor.execute(sql)
    orgs = cursor.fetchall()
    cursor.close()
    if (len(orgs) > 0):
        for next_org in orgs:
            build_dict_by_org_cd(org_dict, next_org[0], conn)
            org_dict[next_org[2]] = next_org
    
def get_sub_orgs(org_id, conn):
    #print(org_id)
    sql = 'select child_org_id from org_relation where parent_org_id = ' + org_id.__str__()
    cursor = conn.cursor()
    cursor.execute(sql)
    orgs = cursor.fetchall()
    cursor.close()
    sub_orgs = list()
    if (len(orgs) > 0):
        more_orgs = list()
        for next_org_id in orgs:
            sub_sub_orgs = more_orgs.__add__(get_sub_orgs(next_org_id[0], conn))
            sub_orgs.append(next_org_id[0])
            sub_orgs = sub_orgs + sub_sub_orgs
    return(sub_orgs)
    
def count_pos_activities(pos, conn):
    sql = 'select count(*) '
    sql += 'from org_position_activity '
    sql += 'where org_position_id = ' + pos.__str__() + ' '
    sql += 'and eff_date <= sysdate '
    sql += 'and (end_date > sysdate or end_date is null)'
    
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchone()
    cursor.close()
    return data[0]

def get_org_pos(org_id, conn):
    sql = 'select op.org_position_id, op.org_position_cd, op.org_position_name,'
    sql += 'oe.org_entry_id, oe.org_entry_cd, oe.org_entry_name '
    sql += 'from org_position op, org_position_status os, org_entry oe '
    sql += 'where os.status_id = 1 '
    sql += 'and oe.org_entry_id = op.org_entry_id '
    sql += 'and os.org_position_id = op.org_position_id '
    sql += 'and os.eff_date <= sysdate '
    sql += 'and (os.end_date > sysdate or os.end_date is null) '
    sql += 'and op.org_entry_id = ' + org_id.__str__()

    
    cursor = conn.cursor()
    cursor.execute(sql)
    pos = cursor.fetchall()
    all_pos = dict()
    cursor.close()
    if (len(pos) > 0):
        for next_pos in pos:
            all_pos[next_pos[1]] = next_pos
            
    return all_pos
