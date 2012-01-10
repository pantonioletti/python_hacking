'''
Created on Feb 1, 2010

@author: pantonio
'''
from org_api import org_entry_small

def load_conf_positions(file):
    try:
        fd = open(file,'r')
        str = fd.readline()
        d_orgs = dict()
        #0: pos_id : 10000000
        #1: pos_name : Promotor
        #2: org_name : Zapatillas Tercero
        #3: org_cd : PEDP0040D317

        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            
            org_cd = vals[3]
            if (org_cd in d_orgs):
                new_org = d_orgs[org_cd]
            else:
                new_org = org_entry_small()
                new_org.name = vals[2]
                new_org.code = org_cd
                d_orgs[org_cd] = new_org
            pos_cd = vals[0]
            if (not pos_cd in new_org.positions):
                new_org.positions[pos_cd] = vals[1]
            str = fd.readline()
        fd.close()
        return d_orgs
    except IOError:
        print ("File ", file, " not found")

def read_conf_positions(file, db_pos):
    try:
        fd = open(file,'r')
        str = fd.readline()
        #0: pos_id : 10000000
        #1: pos_name : Promotor
        #2: org_name : Zapatillas Tercero
        #3: org_cd : PEDP0040D317

        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            org_cd = vals[3]
            if (org_cd in db_pos):
                pos_cd = vals[0]
                if (pos_cd not in db_pos[org_cd].positions):
                    print("This positions does not exist in DB: " + vals[0] + " |" + vals[1] + " |" + vals[2] + " |" + vals[3])
                else:
                    print(vals[0] + " |" + vals[1] + " |" + vals[2] + " |" + vals[3] + " - OK")
            else:
                print("This positions does not exist in DB: " + vals[0] + " |" + vals[1] + " |" + vals[2] + " |" + vals[3])
            str = fd.readline()
        fd.close()

    except IOError:
        print ("File ", file, " not found")

def read_db_positions(file, db_pos):
    try:
        fd = open(file,'r')
        str = fd.readline()
        #0: pos_id : 31000054
        #1: org_cd : PEUE0040DECA
        #2: org_id : 152
        #3: org_level : 4
        #4: org_name : Deporte y Calzado
        #5: pos_name : Supervisor Comercial

        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            org_cd = vals[1]
            if (org_cd in db_pos):
                pos_cd = vals[0]
                if (pos_cd not in db_pos[org_cd].positions):
                    print("This positions does not exist: " + vals[0] + " |" + vals[1] + " |" + vals[2] + " |" + vals[3]+ " |" + vals[4]+ " |" + vals[5])
                else:
                    print(vals[0] + " |" + vals[1] + " |" + vals[2] + " |" + vals[3]+ " |" + vals[4]+ " |" + vals[5] + " - OK")
            else:
                    print("This org does not exist: " + vals[0] + " |" + vals[1] + " |" + vals[2] + " |" + vals[3]+ " |" + vals[4]+ " |" + vals[5])
            str = fd.readline()
        fd.close()

    except IOError:
        print ("File ", file, " not found")

def load_db_positions(file):
    try:
        fd = open(file,'r')
        str = fd.readline()
        d_orgs = dict()
        #0: pos_id : 31000054
        #1: org_cd : PEUE0040DECA
        #2: org_id : 152
        #3: org_level : 4
        #4: org_name : Deporte y Calzado
        #5: pos_name : Supervisor Comercial

        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            
            org_cd = vals[1]
            if (org_cd in d_orgs):
                new_org = d_orgs[org_cd]
            else:
                new_org = org_entry_small()
                new_org.name = vals[4]
                new_org.code = org_cd
                new_org.id = vals[2]
                d_orgs[org_cd] = new_org
            pos_cd = vals[0]
            if (not pos_cd in new_org.positions):
                new_org.positions[pos_cd] = vals[5]
            str = fd.readline()
        fd.close()
        return d_orgs
    except IOError:
        print ("File ", file, " not found")

