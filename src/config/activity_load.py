'''
Created on 19-10-2009

@author: pantonio
'''
class activity:
    def __init__(self, id, cd, name, level, sched, sche_alone, charge):
        self.id = id
        self.cd = cd
        self.name = name[0:32]
        self.level = level
        self.sched = sched
        self.sched_alone = sche_alone
        self.charge = charge
        self.children = dict()
        
    def add_child(self, child):
        self.children[child.id] = child
        
    def sql_insert(self, date):
        sql1= "INSERT INTO ACTIVITY_ENTRY ( ACTIVITY_ENTRY_ID, ACTIVITY_ENTRY_CD, ACTIVITY_ENTRY_NAME, RANK, ACTIVITY_LEVEL_ID, CHARGE_P, SCHEDULE_P, SCHEDULE_ALONE_P ) VALUES ("
        sql1+= self.id.__str__() + ", '" + self.cd + "', '" + self.name[0:31] + "', NULL, " + self.level.__str__() + ", '" + self.charge + "', '" + self.sched + "', '" + self.sched_alone + "');\n"

        sql2 = "INSERT INTO ACT_STATUS ( ACTIVITY_ENTRY_ID, STATUS_ID, EFF_DATE, END_DATE, AUDIT_EMP_ID ) VALUES ("
        sql2 += self.id.__str__() + ", 1,  TO_Date( '" + date + "', 'YYYYMMDD'), NULL, NULL);\n"
        
        if len(self.children) > 0:
            sql3 = ""
            for key in self.children.keys():
                sql3 += "INSERT INTO ACT_RELATION (ACTIVITY_ENTRY_ID, PARENT_ACTIVITY_ENTRY_ID) VALUES ("
                sql3 += self.children[key].id.__str__() + ", " + self.id.__str__() + " );\n"
            
        else:
            sql3 = None
        return (sql1, sql2, sql3)
        
def load_activities(act, path, id, d_act):
    
    try:
        line_counter = 1
        fd = open(act,'r')
        str = fd.readline()
        id_count = id
        d_code_id = dict()
        d_activities = dict()
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            #0:activity_entry_cd;
            #1:activity_entry_name;
            #2:activity_level_id ;
            #3:parent_activity_entry_id ;
            #4:schedule_p ;
            #5:schedule_alone_p ;
            #6:charge_p 
            #id, cd, name, level, sched, sche_alone, charge
            if vals[0] in d_code_id:
                print("!!!!!!! DUPLICATE ACTIVITY!!!!!!!")
                print(vals[0])
            elif vals[0] in d_act:
                pass
            else:
                if (len(vals[1]) > 64):
                    print("-- WARNING - Activity name too long: " + vals[0] + "#" + vals[1])
                    d_code_id[vals[0]] = id_count
                new_act = activity(id_count, vals[0], vals[1], vals[2], vals[4], vals[5], vals[6])
                d_code_id[new_act.cd] = new_act.id
                d_activities[new_act.id] = new_act
                if len(vals[3]) > 0:
                    try:
                        parent_id = d_code_id[vals[3]]
                        d_activities[parent_id].add_child(new_act)
                    except KeyError:
                        print("At line " + line_counter.__str__() + ": parent activity code not found")
                        print(str) 
            id_count += 1
            str = fd.readline()
            line_counter += 1
        fd.close()
        
        activity_entry = open(path + 'activity_entry.sql', 'w')
        act_status = open(path + 'act_status.sql', 'w')
        act_relation = open(path + 'act_relation.sql', 'w')
        
        for key in d_activities.keys():
            sqls = d_activities[key].sql_insert('20050101')
            activity_entry.write(sqls[0])
            act_status.write(sqls[1])
            if (sqls[2] is not None):
                act_relation.write(sqls[2])
                
        activity_entry.close()
        act_status.close()
        act_relation.close()
    except IOError:
        print ("File ", act, " not found")
        
