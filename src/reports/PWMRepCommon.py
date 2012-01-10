import cx_Oracle
#from com.ziclix.python.sql import zxJDBC

## Construye un string de conexion clasico para Oracle
## tipicamente: <usuario>/<passwd>@<servicio>
def buildConnStr(user, passwd, service):
    return user + "/" + passwd + "@" + service

def buildJDBCConnStr(user, passwd, service):
    return "jdbc:oracle:thin:" + user + "/" + passwd + "@" + service

def openConn(connStr):
    db = cx_Oracle.connect(connStr)
    return db

def openConnJDBC(connStr):
    db = zxJDBC.connect(connStr[0], connStr[1], connStr[2], connStr[3])
    return db

def getEmpRotations(conn, rots, emp, start_sdate, end_sdate):
    
    
    empRotSql = "SELECT esr.emp_id, sr.sched_rotation_id, sr.sched_rotation_cd, sr.sched_rotation_name, \
            TO_DATE(esr.eff_sdate, 'yyyymmdd'), TO_DATE(esr.end_sdate, 'yyyymmdd')  \
            FROM emp_sched_rotation esr, sched_rotation sr \
            WHERE esr.eff_sdate < '" + start_sdate + "' \
            AND (esr.end_sdate IS NULL OR esr.end_sdate >= '" + end_sdate + "') \
            AND sr.sched_rotation_id = esr.sched_rotation_id \
            AND sr.sched_rotation_id IN (" + rots + ") \
            AND esr.emp_id in (" + emp + ") \
            ORDER BY esr.emp_id"
       
    rot = conn.cursor()
    rot.execute(empRotSql)
    empRotList = list()
    row = rot.fetchone()
    while(row is not None):
        empRotList.append(row)
        row = rot.fetchone()
    rot.close()
    return empRotList
    
def getDaylyCalendar(conn, org_id, start_date, end_date):
    calSql = "SELECT calendar_id, start_sdate \
            FROM budget_calendar \
            WHERE org_entry_id = " + org_id.__str__() + " \
            AND budget_division_type_id = 1"
    if (end_date is None):
        calSql = calSql + "AND start_sdate >= '" + start_date + "'"
    else:
        calSql = calSql + "AND start_sdate BETWEEN '" + start_date + "' \
                AND '" + end_date + "'"
    
    cal = conn.cursor()
    cal.execute(calSql)
    calList = list()
    
    row = cal.fetchone()
    while(row is not None):
        calList.append(row)
        row = cal.fetchone()
    cal.close()
    return calList


def getBudgetActualValue(conn, org_id, element_id, calendar_id):
    budSql = "SELECT value \
            FROM budget_actual_value \
            WHERE org_entry_id = " + org_id.__str__() + " \
            AND element_id = " + element_id.__str__() + " \
            AND calendar_id = " + calendar_id.__str__()
    
    bud = conn.cursor()
    bud.execute(budSql)
    budList = list()
    
    row = bud.fetchone()
    while(row is not None):
        budList.append(row)
        row = bud.fetchone()
    bud.close()
    return budList

def getSalesLM(conn, org_id, element_id, start_date):
    budSql = "SELECT data_row_id, value \
            FROM budget_detail_import \
            WHERE org_entry_id = " + org_id.__str__() + " \
            AND element_id = " + element_id.__str__() + " \
            AND day_sdate = '" + start_date + "'"
    
    bud = conn.cursor()
    bud.execute(budSql)
    budList = list()
    
    row = bud.fetchone()
    while(row is not None):
        budList.append(row)
        row = bud.fetchone()
    bud.close()
    return budList


def getRotBalanceStatus(conn, org_id, rot_id, start_date, weeks):

    shifts = list()
    for x in range(weeks):
        shifts.append(0)
    bal_sql = "SELECT E.HR_EMP_ID, MOD(TRUNC((SYSDATE - TO_DATE(ESR.EFF_SDATE, 'YYYYMMDD'))/7) + ESR.WEEK_COUNTER, " + weeks.__str__() +") \
            FROM SCHED_ROTATION SR, ORG_SCHED_ROTATION OSR, ORG_POSITION OP, \
            EMP_ORG_POSITION EOP, EMP_SCHED_ROTATION ESR, V_EMP E, EMP_STATUS ES \
            WHERE SR.SCHED_ROTATION_ID = OSR.SCHED_ROTATION_ID \
            AND OP.ORG_ENTRY_ID = OSR.ORG_ENTRY_ID \
            AND EOP.ORG_POSITION_ID = OP.ORG_POSITION_ID \
            AND ESR.SCHED_ROTATION_ID = SR.SCHED_ROTATION_ID \
            AND ESR.EMP_ID = EOP.EMP_ID \
            AND E.EMP_ID = ESR.EMP_ID \
            AND ES.EMP_ID = E.EMP_ID \
\
            AND OSR.EFF_SDATE <= '" + start_date + "' \
            AND (OSR.END_SDATE IS NULL OR OSR.END_SDATE > '" + start_date + "' ) \
\
            AND EOP.EFF_DATE <= TO_DATE('" + start_date + "', 'YYYYMMDD') \
            AND (EOP.END_DATE IS NULL OR EOP.END_DATE > TO_DATE('" + start_date + "', 'YYYYMMDD')) \
\
            AND ESR.EFF_SDATE <= '" + start_date + "' \
            AND (ESR.END_SDATE IS NULL OR ESR.END_SDATE > '" + start_date + "') \
\
            AND ES.EFF_DATE <= TO_DATE('" + start_date + "', 'YYYYMMDD') \
            AND (ES.END_DATE IS NULL OR ES.END_DATE > TO_DATE('" + start_date + "', 'YYYYMMDD')) \
\
            AND ES.EMP_STATUS_ID =1 \
            AND SR.SCHED_ROTATION_ID = " + rot_id.__str__() + " \
            AND OSR.ORG_ENTRY_ID = " + org_id.__str__()
            
    ##print bal_sql
    balance = conn.cursor()
    balance.execute(bal_sql)
    row = balance.fetchone()
    while(row is not None):
        shifts[row[1]] = shifts[row[1]] + 1
        ##print shifts
        row = balance.fetchone()
    balance.close()
    return "Hello world"


# Return type: list
# Por cada registro:
#   pos 0 : ESP.SCHED_PLAN_ID
#   pos 1 : ESP.EFF_SDATE
#   pos 2 : ESP.END_SDATE
#   pos 3 : SP.SCHED_PLAN_CD
#   pos 4 : SP.SCHED_PLAN_NAME
def getSchedPlan(conn, emp_id, start_sdate, end_sdate):
    sched_sql = "SELECT ESP.SCHED_PLAN_ID, ESP.EFF_SDATE, ESP.END_SDATE, sp.sched_plan_cd, sp.sched_plan_name \
                FROM emp_sched_plan esp, sched_plan sp \
                WHERE esp.emp_id = " + emp_id.__str__() + " \
                AND esp.eff_sdate < '" + end_sdate + "' \
                AND (esp.end_sdate is null or esp.end_sdate >= '" + start_sdate + "') \
                AND sp.sched_plan_id = esp.sched_plan_id"
    sched = conn.cursor()
    sched.execute(sched_sql)
    rows = sched.fetchall()
    sched.close()
    return rows

def setSchedPlans(conn, emp, start_sdate, end_sdate):
    sched_sql = "SELECT ESP.SCHED_PLAN_ID, ESP.EFF_SDATE, ESP.END_SDATE, sp.sched_plan_cd, sp.sched_plan_name \
                FROM emp_sched_plan esp, sched_plan sp \
                WHERE esp.emp_id = " + emp.id.__str__() + " \
                AND esp.eff_sdate < '" + end_sdate + "' \
                AND (esp.end_sdate is null or esp.end_sdate >= '" + start_sdate + "') \
                AND sp.sched_plan_id = esp.sched_plan_id"
    sched = conn.cursor()
    sched.execute(sched_sql)
    row = sched.fetchone()
    while(row is not None):
        sp = SchedPlan(row[0],row[3],row[4])
        emp.addSchedPlan(sp)
        row = sched.fetchone()
    sched.close()
    return
    
# Return type: list
# Retorna una lista de Employee
# Asocia cada instancia de Employee a la posicion
def getActiveEmpPos(conn, position, start_sdate, end_sdate):
    emp_sql = "SELECT EOP.EFF_DATE, EOP.END_DATE, EOP.EMP_ID, E.HR_EMP_ID, E.LAST_NAME, E.FIRST_NAME, ES.EFF_DATE, ES.END_DATE " + \
            "FROM EMP_ORG_POSITION EOP, EMP E, EMP_STATUS ES " + \
            "WHERE EOP.ORG_POSITION_ID = " + position.id.__str__() + " "  + \
            "AND EOP.EFF_DATE < TO_DATE('" + end_sdate + "', 'YYYYMMDD') " + \
            "AND (EOP.END_DATE IS NULL OR EOP.END_DATE >= TO_DATE('" + start_sdate + "', 'YYYYMMDD')) " + \
            "AND E.EMP_ID = EOP.EMP_ID " + \
            "AND ES.EMP_ID = E.EMP_ID " + \
            "AND ES.EMP_STATUS_ID = 1 " + \
            "AND ES.EFF_DATE < TO_DATE('" + end_sdate + "', 'YYYYMMDD') " + \
            "AND (ES.END_DATE IS NULL OR ES.END_DATE >= TO_DATE('" + start_sdate + "', 'YYYYMMDD'))"

    #print emp_sql
    emp = conn.cursor()
    emp.execute(emp_sql)
    row = emp.fetchone()
    if (row is None):
        emps = None
    else:
        emps = list()
        while(row is not None):
            employee = Employee(row[2],row[3],row[4],row[5], row[0], row[1])
            employee.addPosition(position)
            emps.append(employee)
            position.addEmp(employee)
            row = emp.fetchone()
    emp.close()
    
    return emps
    

# Return type: list
# Por cada registro:
#   pos 0 : OP.ORG_POSITION_ID,
#   pos 1 : OP.ORG_POSITION_CD
#   pos 2 : OP.ORG_POSITION_NAME
#   pos 3 : OPS.EFF_DATE
#   pos 4 : OPS.END_DATE
def getActivePositions(conn, org_id, start_sdate, end_sdate):
    pos_sql = "SELECT OP.ORG_POSITION_ID, OP.ORG_POSITION_CD, OP.ORG_POSITION_NAME, OPS.EFF_DATE, OPS.END_DATE \
                FROM ORG_POSITION OP, ORG_POSITION_STATUS OPS \
                WHERE OP.ORG_ENTRY_ID = " + org_id.__str__() + " \
                AND OPS.ORG_POSITION_ID = OP.ORG_POSITION_ID \
                AND OPS.STATUS_ID = 1 \
                AND OPS.EFF_DATE < TO_DATE('" + end_sdate + "', 'YYYYMMDD') \
                AND (OPS.END_DATE IS NULL OR OPS.END_DATE >= TO_DATE('" + start_sdate + "', 'YYYYMMDD'))"
    pos = conn.cursor()
    pos.execute(pos_sql)
    row = pos.fetchone()
    if (row is None):
        op = None
    else:
        op = list()
        while(row is not None):
            position = Position(row[0], org_id, row[1], row[2], row[3], row[4])
            position.setActivitiesList(getActivities(conn, row[0], start_sdate, end_sdate)) 
            op.append(position)
            row = pos.fetchone()
    
    pos.close()
    return op

def getActivities(conn, orgpos_id, start_sdate, end_sdate):
    act_sql = "SELECT AE.ACTIVITY_ENTRY_ID, AE.ACTIVITY_ENTRY_CD, AE.ACTIVITY_ENTRY_NAME \
                FROM ORG_POSITION_ACTIVITY OPA, ACTIVITY_ENTRY AE \
                WHERE OPA.ACTIVITY_ENTRY_ID = AE.ACTIVITY_ENTRY_ID \
                AND OPA.ORG_POSITION_ID = " + orgpos_id.__str__() + " \
                AND OPA.EFF_DATE < TO_DATE('" + end_sdate + "', 'YYYYMMDD') \
                AND (OPA.END_DATE IS NULL OR OPA.END_DATE >= TO_DATE('" + start_sdate + "', 'YYYYMMDD'))"
    act = conn.cursor()
    act.execute(act_sql)
    row = act.fetchone()
    if (row is None):
        act_l = None
    else:
        act_l = list()
        while(row is not None):
            act_l.append(Activity(row[0], row[1], row[2]))
            row = act.fetchone()
    
    act.close()
    return act_l
    
# Return type: list
# Por cada registro:
#   pos 0 : osr.org_entry_id
#   pos 1 : osr.sched_rotation_id
#   pos 2 : sr.sched_rotation_cd
#   pos 3 : sr.sched_rotation_name
def getRotations(conn, org_id, start_sdate, end_sdate):
    
    rot_sql = "SELECT osr.org_entry_id, osr.sched_rotation_id, sr.sched_rotation_cd, sr.sched_rotation_name, sr.number_of_weeks \
            FROM org_sched_rotation osr, sched_rotation sr \
            WHERE osr.eff_sdate < '" + start_sdate + "' \
            AND (osr.end_sdate IS NULL OR osr.end_sdate >= '" + end_sdate + "') \
            AND osr.org_entry_id = " + org_id.__str__() + " \
            AND sr.sched_rotation_id = osr.sched_rotation_id"

    rot = conn.cursor()
    rot.execute(rot_sql)
    row = rot.fetchone()
    if (row is None):
        rots = None
    else:
        rots = list()
        while(row is not None):
            new_rot = Rotation(row[1], row[2], row[3], row[4])
            sched_plan_sql = "SELECT SCHED_PLAN_ID FROM SCHED_ROTATION_SCHED_PLAN \
                             WHERE SCHED_ROTATION_ID = " + new_rot.id.__str__()
            spc = conn.cursor()
            spc.execute(sched_plan_sql)
            new_rot.setSchedPlans(spc.fetchall())
            spc.close()
            
            activities_sql = "SELECT SRA.ACTIVITY_ENTRY_ID \
                                FROM SCHED_ROTATION_ACTIVITY SRA \
                                WHERE SRA.SCHED_ROTATION_ID = " + new_rot.id.__str__()
            ac = conn.cursor()
            ac.execute(activities_sql)
            new_rot.setActivitiesList(ac.fetchall())
            ac.close()
            
            rots.append(new_rot)
            row = rot.fetchone()
    
    rot.close()
    return rots

def getAppliedRot(conn, emp_id, start_sdate, end_sdate):
    rot_cursor = conn.cursor()
    
    rot_sql = "SELECT UNIQUE SR.SCHED_ROTATION_ID, SR.SCHED_ROTATION_CD, SR.SCHED_ROTATION_NAME \
                FROM EMP_SCHED_ROTATION ESR, SCHED_ROTATION SR \
                WHERE SR.SCHED_ROTATION_ID = ESR.SCHED_ROTATION_ID \
                AND ESR.EMP_ID = " + emp_id.__str__() + " \
                AND ESR.EFF_SDATE <= '" + end_sdate + "' \
                AND (ESR.END_SDATE IS NULL OR ESR.END_SDATE > '" + start_sdate + "')"

    rot_cursor.execute(rot_sql)
    rows = list()
    rows = rot_cursor.fetchall()
    return rows

# Return type: un org
# Por cada registro:
#   pos 0 : OE.ORG_ENTRY_ID
#   pos 1 : OE.LOCATION_NAME
#   pos 2 : OE.ORG_ENTRY_NAME
#   pos 3 : OE.ORG_ENTRY_CD
#   pos 4 : OL.ORG_LEVEL_CD
def getOrg(conn, org_cd):
    local = conn.cursor()
    
    local_sql = "SELECT OE.ORG_ENTRY_ID, OE.LOCATION_NAME, OE.ORG_ENTRY_NAME, OE.ORG_ENTRY_CD, OL.ORG_LEVEL_CD \
            FROM ORG_ENTRY OE, ORG_LEVEL OL \
            WHERE OE.ORG_ENTRY_CD = '" + org_cd + "' \
            AND OE.ORG_LEVEL_ID = OL.ORG_LEVEL_ID"
    
    local.execute(local_sql, dict())
    rows = local.fetchone()
    org = Org(rows[0], rows[3], rows[2], rows[4], rows[1])
    local.close()
    return org

# Return type: list de intancias de Org
def getOrgChildren(conn, org_id, parent_cd = None, parent_lvl = None):
    local = conn.cursor()
    
    local_sql = "SELECT OE2.ORG_ENTRY_ID, OE2.LOCATION_NAME, OE2.ORG_ENTRY_NAME, \
            OE2.ORG_ENTRY_CD, OL.ORG_LEVEL_CD, TO_CHAR(RO.EFF_DATE, 'MM/DD/YYYY') \
            FROM ORG_ENTRY OE, ORG_RELATION RO, ORG_ENTRY OE2, ORG_LEVEL OL \
            WHERE OE.ORG_ENTRY_ID = " + org_id.__str__() + " \
            AND OE2.ORG_LEVEL_ID = OL.ORG_LEVEL_ID \
            AND RO.PARENT_ORG_ID = OE.ORG_ENTRY_ID \
            AND RO.CHILD_ORG_ID = OE2.ORG_ENTRY_ID \
            AND RO.EFF_DATE < SYSDATE \
            AND RO.END_DATE IS NULL "
    
    local.execute(local_sql)
    
    row = local.fetchone()
    if (row is None):
        orgs = None
    else:
        orgs = list()
        while (row is not None):
            actual = Org(row[0], row[3], row[2], row[4], row[1])
            if (parent_cd is not None):
                actual.setParentRel(parent_cd, parent_lvl, row[5])
            orgs.append(actual)
            row = local.fetchone()
    
    local.close()
    return orgs
    
def getOrgAttr(conn, org_id, attr_id):
    
    attr = conn.cursor()
    
    attr_sql = "SELECT OAV.ATTRIBUTE_VALUE \
            FROM ORG_ATTRIBUTE_VALUE OAV \
            WHERE OAV.ATTRIBUTE_ID = " + attr_id.__str__() + " \
            AND OAV.ORG_ENTRY_ID = " + org_id.__str__()
    
    attr.execute(attr_sql)
    
    row = attr.fetchone()
    if (row is None):
        val = None
    else:
        val = row[0]
    
    attr.close()
    return val

def valOrgPos(conn, org_id, attr_id, attr_val, pos_cd, start_date, end_date):
    
    pos = conn.cursor()
    
    pos_sql = "SELECT OAV.ATTRIBUTE_VALUE \
            FROM ORG_ATTRIBUTE_VALUE OAV, ORG_POSITION OP, ORG_POSITION_STATUS OPS \
            WHERE OAV.ATTRIBUTE_ID = " + attr_id.__str__() + " \
            AND OP.ORG_ENTRY_ID = OAV.ORG_ENTRY_ID \
            AND OPS.ORG_POSITION_ID = OP.ORG_POSITION_ID \
            AND OAV.ORG_ENTRY_ID = " + org_id.__str__() + " \
            AND OAV.ATTRIBUTE_VALUE = '" + attr_val + "' \
            AND OP.ORG_POSITION_CD = '" + pos_cd + "' \
            AND OPS.STATUS_ID = 1 \
            AND OPS.EFF_DATE <= TO_DATE('" + end_date + "', 'YYYYMMDD') \
            AND (OPS.END_DATE IS NULL OR OPS.END_DATE > TO_DATE('" + start_date + "', 'YYYYMMDD'))"
            
    pos.execute(pos_sql)
    
    row = pos.fetchone()
    if (row is None):
        val = False
    else:
        val = True
    
    pos.close()
    return val

def getAllChildren(connStr, org_cd):
    conn = openConn(connStr)
    all = getAllChildrenConn(conn, org_cd)
    conn.close()
    return all

def getAllChildrenConn(conn, org_cd):
    all = list()
    all.append(getOrg(conn, org_cd))

    i = 0
    while (i < len(all)):
        tmp = getOrgChildren(conn, all[i].id, all[i].code, all[i].level)
        if (tmp is not None):
            all.extend(tmp)
        i+=1
    return all


class Org:
    def __init__(self, org_id, org_cd, org_name, org_level, location_name):
        self.id = org_id
        self.code = org_cd
        self.name = org_name
        self.level = org_level
        self.location = location_name
        self.attr12 = None
        self.parent_cd = None
        self.parent_level = None
        self.parent_eff_date = None
    def setParentRel(self, code, level, eff_date):
        self.parent_cd = code
        self.parent_level = level
        self.parent_eff_date = eff_date
    def setAttr12(self, attr_val):
        self.attr12 = attr_val
    def print_me(self):
        return "ORG: " + self.code + "  " + self.name + "\n"
    
class Position:
    def __init__(self, org_position_id, org_entry_id, org_position_cd, org_position_name, start_date, end_date):
        self.id = org_position_id
        self.org_id = org_entry_id
        self.code = org_position_cd
        self.name = org_position_name
        self.start = start_date
        self.end = end_date
        self.emps = dict()
        self.activities = list()
        
    def setActivitiesList(self, activities):
        self.activities = activities
        
    def addEmp(self, emps):
        self.emps[id] = emps

    def print_me(self):
        return "POSITION: CODE => " + self.code + "  " + self.name

    def printPosition(self):
        print ("POSITION: CODE => ", self.code, " || NAME=> ", self.name)

class Rotation:
    def __init__(self, sched_rotation_id, sched_rotation_cd, sched_rotation_name, num_of_weeks):
        self.id = sched_rotation_id
        self.code = sched_rotation_cd
        self.name = sched_rotation_name
        self.sched_plans = list()
        self.activities = list()
        self.weeks = num_of_weeks

    def setActivitiesList(self, activities):
        self.activities = activities
        
    def setSchedPlans(self, sched_plans):
        self.sched_plans.extend(sched_plans)
        
    def print_me(self):
        return "ROTATION: " + self.code + "  " + self.name

    def printRotation(self):
        print (self.code)

class Activity:
    def __init__(self, activity_id, activity_cd, activity_name):
        self.id = activity_id
        self.code = activity_cd
        self.name = activity_name
    def print_me(self):
        return "ACTIVITY: " + self.code + "  " + self.name

class SchedPlan:
    def __init__(self, sched_plan_id, sched_plan_cd, sched_plan_name):
        self.id = sched_plan_id
        self.code = sched_plan_cd
        self.name = sched_plan_name
        self.schedplan = int(0)

    def print_me(self):

        return "SCHEDULE PLAN: " + self.code + "  " + self.name
        
class Employee:
    def __init__(self, emp_id, hr_emp_id, emp_last_name, emp_first_name, eff_date, end_date):
        self.id = emp_id
        self.hr_id = hr_emp_id
        self.last = emp_last_name
        self.first = emp_first_name
        self.eff_date = eff_date
        self.end_date = end_date
        self.sched_plans = dict()
        self.pos = dict()
        self.qual_rot = dict()
        self.applied_rot = list()
        self.no_rotation = False

    def setNoRotation(self):
        self.no_rotation = True

    def setAppliedRot(self, applied):
        self.applied_rot.extend(applied)
        
    def getActivities(self):
        activities = dict()
        posIter = self.pos.itervalues()
        while(True):
            try:
                position = posIter.next()
                if (position.activities is not None):
                    for i in range(0, len(position.activities)):
                        activities[position.activities[i].id] = position.activities[i]
            except StopIteration:
                break
        return activities
    
    def addSchedPlan(self, sp):
        self.sched_plans[sp.id] = sp
    
    def addPosition(self, pos):
        self.pos[pos.id] = pos
         
    def addQualifyingRot(self, rot):
        self.qual_rot[rot.id] = rot
           
    def print_me(self):
        str = "HR ID: " + self.hr_id + " - " + self.last + "  " + self.first + "\n"
        str +="    Position(s): \n"

        pos_iter = self.pos.itervalues()
        while(True):
            try:
                position = pos_iter.next()
                str += "            " + position.print_me() + "\n"
            except StopIteration:
                break

        str+= "    Schedule plan(s): \n"
        sched_iter = self.sched_plans.itervalues()
        while(True):
            try:
                sched = sched_iter.next()
                str += "            " + sched.print_me() + "\n"
            except StopIteration:
                break

        str += "    Qualify for these rotations: \n"
        rot_iter = self.qual_rot.itervalues()
        while(True):
            try:
                rotation = rot_iter.next()
                str += "            " + rotation.print_me() + "\n"
            except StopIteration:
                break
            
        if (self.no_rotation):
            str += "    HAS NO ROTATION\n"
        else:
            str += "    Has the following rotations: \n"
            for i in range(0, len(self.applied_rot)):
                str += self.applied_rot.__str__() + "\n"
            
        return str

    def printEmployee(self):
        print ("HR ID: ", self.hr_id, " || LAST NAME : ", self.last, " || FIRST NAME: ", self.first)
        print ("    Position(s): ")

        pos_iter = self.pos.itervalues()
        while(True):
            try:
                position = pos_iter.next()
                print ("            ", position.code, " ", position.name)
            except StopIteration:
                break

        print ("    Schedule plan(s): ")
        sched_iter = self.sched_plans.itervalues()
        while(True):
            try:
                sched = sched_iter.next()
                print ("            ", sched.code, " ", sched.name)
            except StopIteration:
                break

        print ("    Qualify for these rotations: ")
        rot_iter = self.qual_rot.itervalues()
        while(True):
            try:
                rotation = rot_iter.next()
                print ("            ", rotation.code, " ", rotation.name)
            except StopIteration:
                break
