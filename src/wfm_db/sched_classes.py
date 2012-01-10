'''
Created on Mar 25, 2010

@author: pantonio
'''
class Emp:
    def __init__(self, emp_id, hr_emp_id, last_name, first_name):
        self.id = emp_id
        self.hr_id = hr_emp_id
        self.first = first_name
        self.last = last_name

class Rotation:
    def __init__(self, rot_id, rot_cd, rot_name, rot_type):
        self.id = rot_id
        self.cd = rot_cd
        self.name = rot_name
        self.type = rot_type
        self.orgs = list()
        self.sched_plan = list()
        self.activities = list()
  
    def r_print(self):
        str = 'Id: ' + self.id.__str__()
        str += ' || Code: ' + self.cd
        str += ' || Name: ' + self.name
        str += ' || Type: ' + self.type.__str__()
        str += ' || Sched plan: ['
        for sp in self.sched_plan:
            str += sp.__str__() + ','
        str += '] || Activities: '
        for act in self.activities:
            str += act.__str__() + ','
        str += '] || Orgs: '
        for org in self.orgs:
            str += org.__str__() + ','
        str += ']'
        print(str)
        
    def add_org(self, org_id):
        if (org_id not in self.orgs):
            self.orgs.append(org_id)
        
    def add_sched_plan(self, sp_id):
        if (sp_id not in self.sched_plan):
            self.sched_plan.append(sp_id)
        
    def add_activity(self, act_id):
        if (act_id not in self.activities):
            self.activities.append(act_id)
        
class Org:
    def __init__(self, org_id, org_cd, org_name):
        self.id = org_id
        self.cd = org_cd
        self.name = org_name
        
