'''
Created on Jul 20, 2010

@author: pantonio
'''
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta

month = {1:'Enero',2:'Febrero', 3:'Marzo', 4:'Abril', 5:'Mayo', 6:'Junio', 7:'Julio', 8:'Agosto', 9:'Septiembre', 10:'Octubre', 11:'Noviembre', 12:'Diciembre'}
days = {0:'Lunes', 1:'Martes',2:'Miercoles', 3:'Jueves', 4:'Viernes', 5:'Sabado', 6:'Domingo'}

class day:
    def __init__(self, d_date):
        self.d_date = d_date
        self.shift = None
    def to_str(self):
        s = days[self.d_date.weekday()] + " " + self.d_date.day.__str__() + " " + month[self.d_date.month] + "\n"
        if self.shift is not None:
            s += self.shift.s_date.hour.__str__() + ":" + self.shift.s_date.minute.__str__() + " - "
            s += self.shift.e_date.hour.__str__() + ":" + self.shift.e_date.minute.__str__()
        return s
    
class week:
    def __init__(self, s_date):
        self.start = s_date
        self.end = self.start + timedelta(days=6)
        self.days = tuple([day(self.start), \
                           day(self.start + timedelta(days=1)),
                           day(self.start + timedelta(days=2)),
                           day(self.start + timedelta(days=3)),
                           day(self.start + timedelta(days=4)),
                           day(self.start + timedelta(days=5)),
                           day(self.start + timedelta(days=6))])
    def add_shift(self, s):
        d = s.s_date.date()
        if d < self.start or d > self.end:
            print ("Wrong shift assigement " + s.id.__str__())
            return
        delta = d - self.start
        self.days[delta.days].shift = s

    def pprint(self):
        for d in range(len(self.days)):
            print(self.days[d].to_str())
             

class emp:
    def __init__(self, id, hr_id, last, first):
        self.id = id
        self.hr_id = hr_id
        self.last = last
        self.first = first
        self.weeks = dict()
    def init_weeks(self, nw, sdate):
        d = sdate
        delta = timedelta(days=7)
        for w in range(nw):
            self.weeks[w] = week(d)
            d = d + delta
    def add_shift(self, s):
        s_date= s.s_date.date()
        for w in range(len(self.weeks)):
            if self.weeks[w].start <= s_date and self.weeks[w].end >= s_date:
                self.weeks[w].add_shift(s) 
        
    def pprint(self):
        s = self.last + " " + self.first + "\n" + self.hr_id
        print(s)
        for sk in self.weeks.keys():
            self.weeks[sk].pprint()
        print("--------------------------------------------------------")

class shift:
    def __init__(self, id, s_day, s_mday, s_month, s_year, s_time, e_day, e_mday, e_month, e_year, e_time):
        self.id =id
        hr_mi = s_time.split(':')
        self.s_date = datetime(int(s_year), int(s_month), int(s_mday), hour=int(hr_mi[0]), minute=int(hr_mi[1]))
        hr_mi = e_time.split(':')
        self.e_date = datetime(int(s_year), int(s_month), int(s_mday), hour=int(hr_mi[0]), minute=int(hr_mi[1]))
        self.b_sdate = None
        self.b_edate = None
        self.b_type = None
    def add_break(self, t_break):
        if len(t_break) > 0:
            hr_mi = t_break[0].split(':')
            self.b_sdate = time(hour=int(hr_mi[0]), minute=int(hr_mi[1]))
            hr_mi = t_break[1].split(':')
            self.b_edate = time(hour=int(hr_mi[0]), minute=int(hr_mi[1]))
    def pprint(self):
        s = self.s_day + " " + self.s_date.day + " de " + month[self.s_date.month] + "\n"
        s += "Inicio: " + self.s_date.hour + ":" + self.s_date.minute + "  Fin: " +self.e_date.hour + ":" + self.e_date.minute  + "\n"
        s += "Receso : " + self.b_sdate.hour + ":" + self.b_sdate.minute + " - " + self.b_edate.hour + ":" + self.b_edate.minute 
        
        print(s)
        
def emp_multiweek_rep(s_date, e_date, conn):
    
    start_date = date(int(s_date[0:4]), int(s_date[4:6]), int(s_date[6:8]))
    end_date = date(int(e_date[0:4]), int(e_date[4:6]), int(e_date[6:8]))
    
    delta = end_date - start_date + timedelta(days=1)
    if delta.days < 1:
        print("First start date, then end date")
        return None
    if delta.days%7 != 0:
        print("end date - start date should be mutiple of 7")
        return None
    if start_date.weekday() != 0:
        print("start date should be a Monday")
        return None
    weeks = int(delta.days/7)
    
    

    sql = "select e.hr_emp_id, e.last_name, e.first_name, s.shift_id, TO_CHAR(s.start_date, 'DAY'), TO_CHAR(s.start_date, 'dd'), " 
    sql += "TO_CHAR(s.start_date, 'mm'), TO_CHAR(s.start_date, 'yyyy'), to_char(s.start_date - (4/24), 'hh24:mi'), " 
    sql += "to_char(s.end_date - (4/24), 'hh24:mi'),s.start_date, s.end_date, e.emp_id "
    sql += "from shift s, emp e  "
    sql += "where e.emp_id = s.emp_id " 
    sql += "and s.shift_state_type_id = 2 " 
    sql += "and s.start_date - (4/24) > to_date('" + s_date + "','yyyymmdd') " 
    sql += "and s.end_date - (4/24) < to_date('" + e_date + "','yyyymmdd')  "
    sql += "order by e.hr_emp_id, s.start_date, s.end_date"
    
    
    cursor = conn.cursor()
    emps = dict()
    
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    if (len(data) > 0):
        for next_rot in data:
            if not next_rot[12] in emps:
                e = emp(next_rot[12],next_rot[0],next_rot[1],next_rot[2])
                e.init_weeks(weeks, start_date)
                emps[e.id] = e
            #id, s_day, s_mday, s_month, s_year, s_time, e_day, e_mday, e_month, e_year, e_time
            new_shift = shift(next_rot[3], next_rot[4], next_rot[5], next_rot[6], next_rot[7], next_rot[8],\
                              None, None, None, None, next_rot[9])
            new_shift.add_break(get_break(new_shift.id, conn))
            emps[next_rot[12]].add_shift(new_shift)
    return emps

    
def get_break(shift_id, conn):
    
    sql = "select to_char(sb.break_start_date-(4/24),'hh24:mi'), to_char(sb.break_end_date-(4/24),'hh24:mi') "
    sql += "from shift_break sb "
    sql += "where sb.shift_id = " + shift_id.__str__()
    
    #print(sql)
    cursor = conn.cursor()
    
    cursor.execute(sql)
    try:
        data = cursor.fetchone()
    except Exception:
        data = None
    cursor.close()
    
    return data
    