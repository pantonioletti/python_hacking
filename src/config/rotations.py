#coding=ISO_8859-1
'''
Created on May 11, 2010

@author: pantonio
'''
week_days={'SU':0,'MO':1,'TU':2,'WE':3,'TH':4,'FR':5,'SA':6}
days_seq=['SU','MO','TU','WE','TH','FR','SA']
day_conv={0:1,1:2,2:3,3:4,4:5,5:6,6:0}
rot_types = {'AVAIL':'1','SHIFT':'2'}
class day_hours:
    def __init__(self, day, start, end):
        self.day = day
        self.start = start
        self.end = end
        
class rotation:
    def __init__(self, code, name, type, schedp, act, weeks):
        self.code = code
        self.name = name
        self.type = type
        self.weeks = weeks
        self.sched_plan = schedp
        self.activity = act
        self.weeks_hours = dict()
        self.sched_plan_s = set()
        self.activity_s = set()

    def add_sched_plan(self, sp_id):
        self.sched_plan_s.add(sp_id)
        
    def add_activity(self, act_id):
        self.activity_s.add(act_id)
        
    def printr2(self, act_d, sp_d):
        print('Rotation Code;' + self.code)
        print('Rotation Name;' + self.name)
        print('Type Rotation;' + self.type)
        str = ''
        while len(self.sched_plan_s) > 0:
            sp_id = self.sched_plan_s.pop()
            if sp_id in sp_d:
                str += ';' + sp_d[sp_id][0]
        if len(str) == 0:
            str = ';;Not in defined Schedule Plans'
            
        print('Schedule Plan Code :' + str)
        str = ''
        while len(self.activity_s) > 0:
            act_id = self.activity_s.pop()
            if act_id in act_d:
                str += ';' + act_d[act_id][0]
        if len(str) == 0:
            str = ';;Not in defined Activities'
        print('Activity Code :' + str)
        print('Week;Lunes;Martes;Miércoles;Jueves;Viernes;Sábado;Domingo')
        for week in range(1, int(self.weeks) + 1):
            str = week.__str__() + ';'
            key = week.__str__()
            if '2' in self.weeks_hours[key]:
                str += self.weeks_hours[key]['2'].start + ' - ' + self.weeks_hours[key]['2'].end
            str += ';'
            if '3' in self.weeks_hours[key]:
                str += self.weeks_hours[key]['3'].start + ' - ' + self.weeks_hours[key]['3'].end
            str += ';'
            if '4' in self.weeks_hours[key]:
                str += self.weeks_hours[key]['4'].start + ' - ' + self.weeks_hours[key]['4'].end
            str += ';'
            if '5' in self.weeks_hours[key]:
                str += self.weeks_hours[key]['5'].start + ' - ' + self.weeks_hours[key]['5'].end
            str += ';'
            if '6' in self.weeks_hours[key]:
                str += self.weeks_hours[key]['6'].start + ' - ' + self.weeks_hours[key]['6'].end
            str += ';'
            if '7' in self.weeks_hours[key]:
                str += self.weeks_hours[key]['7'].start + ' - ' + self.weeks_hours[key]['7'].end
            str += ';'
            if '1' in self.weeks_hours[key]:
                str += self.weeks_hours[key]['1'].start + ' - ' + self.weeks_hours[key]['1'].end
            print(str)

    def printr(self):
        print('Code : ' + self.code)
        print('Name : ' + self.name)
        print('Type : ' + self.type)#self.types[self.type])
        
        for week_num in self.weeks_hours.keys(): #range(int(self.weeks)):
            week = self.weeks_hours[week_num]
            str = ''
            for day in days_seq:
                str += day
                if week[week_days[day]] is None:
                    str += ' free '
                else:
                    str += ' begin: ' + week[week_days[day]].start + '  end: ' + week[week_days[day]].end + ' '
            print(str) 
            
    def print_sql(self, id):
        sql = str()
        sql += "insert into sched_rotation (SCHED_ROTATION_ID,SCHED_ROTATION_CD,SCHED_ROTATION_NAME,NUMBER_OF_WEEKS,"
        sql += "ALL_DAYS_P,DAY1_P,DAY2_P,DAY3_P,DAY4_P,DAY5_P,DAY6_P,DAY7_P,SCHED_ROTATION_TYPE_ID) "
        sql += "values (" + id.__str__() + ",'" + self.code + "','" + self.name + "'," + self.weeks.__str__() + ",'Y','N','N','N','N','N','N','N'," + self.type + ");\n"
        sp_it = iter(self.sched_plan_s)
        for sp_id in sp_it:
            sql += "insert into sched_rotation_sched_plan (SCHED_ROTATION_ID,SCHED_PLAN_ID) "
            sql += "values (" + id.__str__() + "," + sp_id.__str__() + ");\n"
        if int(self.type) == 2:
            act_it = iter(self.activity_s)
            for act_id in act_it:
                sql += "insert into sched_rotation_activity (sched_rotation_id, activity_entry_id) values ("
                sql += id.__str__() + "," + act_id.__str__() + ");\n"
        for week_num in range(1, int(self.weeks)+1):
            for day in range(7):
                if self.weeks_hours[week_num.__str__()][day] is not None:
                    sql += "insert into sched_rotation_detail (SCHED_ROTATION_ID,SCHED_ROTATION_WEEK,DAY_ID,"
                    sql += "START_STIME,END_STIME,ACTIVITY_ENTRY_ID) "
                    sql += "values (" + id.__str__() + ", " + week_num.__str__() + ", " + (day + 1).__str__() 
                    sql += ",'" + self.weeks_hours[week_num.__str__()][day].start + "','" + self.weeks_hours[week_num.__str__()][day].end + "'," 
                    if int(self.type) == 2:
                        sql += act_id.__str__()
                    else:
                        sql += "NULL"
                    sql += ");\n"
        return sql
    
def load_rotations3(file, d_s_plans, d_act):
#    RC;TESORER_AHUM;;;;;;
#    RN;Depto Tesoreria Ahumada;;;;;;
#    TR;SR|AR;;;;;;
#    SPC;FT45_F;;;;;;
#    AC;TESORERIA;;;;;;
#    Week;Lunes;Martes;Miércoles;Jueves;Viernes;Sábado;Domingo
#    1;1000-2100;1000-2100;1000-1530;;;1000-2100;1000-2100
#    2;1000-1530;;;1000-2100;1000-2100;1000-2100;1000-2100
#    3;;1000-2100;1000-2100;1000-2100;1000-2100;1000-1530;
#    4;1000-2100;1000-2100;1000-2100;1000-2100;1000-1530;;
    try:
        fd = open(file, 'r')
        str = fd.readline()
        d_rot = dict()
        rot_id = 1
        curr_rot = rotation(None, None, None, None, None, None)
        ok = True
        while(len(str)!= 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            if vals[0] == 'RC':
                curr_rot = rotation(None, None, None, None, None, None)
                if len(vals[1].strip()) > 0:
                    curr_rot.code = vals[1].strip()
                    ok = True
                else:
                    ok = False
            elif vals[0] == 'RN' and ok:
                curr_rot.name = vals[1].strip()
            elif vals[0] == 'TR' and ok:
                curr_type = vals[1].strip()
                if curr_type in rot_types:
                    curr_rot.type = rot_types[curr_type]
                else:
                    ok = False
            elif vals[0] == 'SPC' and ok:
                for i in range(1, len(vals)):
                    sp_cd = vals[i].strip()
                    if len(sp_cd) > 0:
                        if sp_cd in d_s_plans:
                            curr_rot.add_sched_plan(d_s_plans[sp_cd])
                        else:
                            print("Error, schedule plan doesn´t exist:\n" + str)
            elif vals[0] == 'AC' and ok:
                for i in range(1, len(vals)):
                    act_cd = vals[i].strip()
                    if len(act_cd) > 0:
                        if act_cd in d_act:
                            curr_rot.add_activity(d_act[act_cd])
                        else:
                            print(curr_rot.code + " " + curr_rot.name + " " + act_cd)
                            #print("Error, activity doesn´t exist:\n" + str)
            elif vals[0] == 'Week' and ok:
                pass
            elif ok:
                if vals[0].isdigit():
                    curr_rot.weeks_hours[vals[0]]= {0:None,1:None,2:None,3:None,4:None,5:None,6:None}
                    for day in range(1, len(vals)):
                        new_day = None
                        if len(vals[day].strip()) > 0:
                            hours = vals[day].rsplit('-')
                            new_day = day_hours(day_conv[day-1], hours[0], hours[1])
                            curr_rot.weeks_hours[vals[0]][new_day.day] = new_day 
                            
                else:
                    print("Error, expecting a week schedule but got this:\n" + str)
            curr_rot.weeks = len(curr_rot.weeks_hours)
            d_rot[curr_rot.code] = curr_rot
            str = fd.readline()
        fd.close()
        ids = 100
        for rot_cd in d_rot.keys():
            print(d_rot[rot_cd].print_sql(ids))
            ids += 1
    except IOError:
        print ("File ", file, " not found")
    return d_rot    

def load_rotations2(file):
    # 0: 1034_1 (code)   
    # 1: Encargado de Administracion 1 (name)
    # 2: 1 (weeks)
    # 3: Shift Rotation (rotation type)
    # 4: 1 (week number)
    # 5: 2 (day number)
    # 6: 0900 (start hour)
    # 7: 1900 (end hour)
    # 8: 4 (schedule plan)
    # 9: 313 (activity)
    try:
        act_d = dict()
        fd = open('C:/dev/projects/ScriptsUtil/data/input/activity_ids_fala.txt')

        str = fd.readline()
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            act_l = list()
            act_l.append(vals[1])
            act_l.append(vals[2])
            act_d[vals[0]] = act_l
            str = fd.readline()
        fd.close()

        sp_d = dict()
        fd = open('C:/dev/projects/ScriptsUtil/data/input/sched_plan_ids_fala.txt')
        str = fd.readline()
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            sp_l = list()
            sp_l.append(vals[1])
            sp_l.append(vals[2])
            sp_d[vals[0]] = sp_l
            str = fd.readline()
        fd.close()

        fd = open(file, 'r')
        str = fd.readline()
        d_rot = dict()
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            if vals[0] not in d_rot:
                d_rot[vals[0]] = rotation(vals[0],vals[1], vals[3], None, None, vals[2])
            if vals[4] not in d_rot[vals[0]].weeks_hours:
                d_rot[vals[0]].weeks_hours[vals[4]]= dict()
            d_rot[vals[0]].weeks_hours[vals[4]][vals[5]] = day_hours(vals[5],vals[6],vals[7])
            d_rot[vals[0]].add_sched_plan(vals[8])
            d_rot[vals[0]].add_activity(vals[9])
                
            str = fd.readline()
        fd.close()
        
        for rot in d_rot.keys():
            d_rot[rot].printr2(act_d, sp_d)
            print(';')
    except IOError:
        print ("File ", file, " not found")
    return d_rot    

def load_rotations(file, d_act, d_sp, conn):
    # 0: C45FO-04; (code)
    # 1: Secretaria; (name)
    # 2: C45FO; (sched plan)
    # 3: GERENCIA; (org)
    # 4: 2; (1|2)
    # 5: 1; (weeks)
    # 6: OP-8002 (activity)
    try:
        fd = open(file, 'r')
        str = fd.readline()
        d_rot = dict()
        rot_id = 1
        cur = conn.cursor()
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            act_id = 0
            ok = True
            #print("=>" + vals[0] + "<=>" + vals[1]+ "<=>" + vals[4] + "<=")
            if int(vals[4]) == 2:
                if vals[6] in d_act:
                    act_id = d_act[vals[6]]
                else:
                    print('Rotation ' + vals[0] + ' has no activity associated')
                    ok = False
            sp_id = 0
            if vals[2] in d_sp:
                sp_id = d_sp[vals[2]]
            else:
                print('Rotation ' + vals[0] + ' has no schedule plan associated')
                ok = False
            rot = rotation(vals[0], vals[1], vals[4], sp_id, act_id, vals[5])
            for idx in range(int(rot.weeks)):
                hours = dict()
                str = fd.readline()
                str = str.replace('\n', '')
                vals = str.rsplit(';')
                for day in range(7):
                    if vals[day+1] == 'Libre':
                        hours[day_conv[day]] = None
                    else:
                        ftm_hr = vals[day+1].replace(':','')
                        hours[day_conv[day]] = ftm_hr.rsplit('-')
                #1;00:00-00:00;00:00-00:00;Libre;00:00-00:00;00:00-00:00;00:00-00:00;Libre
                rot.weeks_hours[idx] = hours
            if ok:
                sqls = rot.print_sql(rot_id)
                for sql in sqls:
                    #print(sql)
                    cur.execute(sql)
                d_rot[rot.code]=rot
                rot_id += 1
            str = fd.readline()
        cur.close()
        fd.close()
    except IOError:
        print ("File ", file, " not found")
    return d_rot    
