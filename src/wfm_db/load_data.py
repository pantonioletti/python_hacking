'''
Created on May 11, 2010

@author: pantonio
'''
def get_activities(conn):
    
    sql = 'select ae.activity_entry_cd, ae.activity_entry_id '
    sql += 'from activity_entry ae'
    
    cursor = conn.cursor()
    cursor.execute(sql)
    acts = cursor.fetchall()
    dact = dict()
    cursor.close()
    if (len(acts) > 0):
        for next_act in acts:
            dact[next_act[0]] = next_act[1]
            
    return dact

def get_days(conn):
    
    sql = 'select day_id, day_cd, day_name '
    sql += 'from day_of_week'
    cursor = conn.cursor()
    cursor.execute(sql)
    days = cursor.fetchall()
    cursor.close()
    ddays = dict()
    if len(days)> 0:
        for next_day in days:
            ddays[next_day[1]] = next_day[0]
    return ddays

def get_severity(conn):
    
    sql = 'select severity_id, severity_cd, severity_name'
    sql += 'from severity_type'
    cursor = conn.cursor()
    cursor.execute(sql)
    sev = cursor.fetchall()
    cursor.close()
    dsev = dict()
    if len(sev)> 0:
        for next_sev in sev:
            dsev[next_sev[1]] = next_sev[0]
    return dsev

def get_pay_plan_type(conn):
    
    sql = 'select pay_plan_type_id, pay_plan_type_cd, pay_plan_type_name '
    sql += 'from pay_plan_type'
    cursor = conn.cursor()
    cursor.execute(sql)
    ptype = cursor.fetchall()
    cursor.close()
    dptype = dict()
    if len(ptype)> 0:
        for next_type in ptype:
            dptype[next_type[1]] = next_type[0]
    return dptype


def get_max_act_id(conn):
    
    sql = 'select max(ae.activity_entry_id) '
    sql += 'from activity_entry ae'
    
    cursor = conn.cursor()
    cursor.execute(sql)
    acts = cursor.fetchone()
    max_id = None
    if (len(acts) > 0):
        max_id = acts[0]
            
    return max_id

def get_max_pay_plan_id(conn):
    
    sql = 'select max(pay_plan_id) '
    sql += 'from pay_plan'
    
    cursor = conn.cursor()
    cursor.execute(sql)
    payp = cursor.fetchone()
    max_id = None
    if (len(payp) > 0):
        max_id = payp[0]
            
    return max_id

def get_sched_plan(conn):
    
    sql = "select sp.sched_plan_cd, sp.sched_plan_id "
    sql += "from sched_plan sp"

    cursor = conn.cursor()
    cursor.execute(sql)
    sps = cursor.fetchall()
    dsp = dict()
    cursor.close()
    if (len(sps) > 0):
        for next_sp in sps:
            dsp[next_sp[0]] = next_sp[1]
            
    return dsp
