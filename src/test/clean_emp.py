'''
Created on 03-04-2012

@author: pantonio
'''
from sys import argv

if __name__ == '__main__':
    f_db = open(argv[1], 'r')
    f_int = open(argv[2],'r')
    hr_id = f_int.readline()
    emp_int = set()
    
    while len(hr_id)!=0:
        hr_id = hr_id.replace('\n','')
        emp_int.add(hr_id)
        hr_id = f_int.readline()
    f_int.close()

    #print("Interface employees: " + len(emp_int).__str__())

    db_ids = f_db.readline()
    db_set = set()
    to_rem = set()

    while len(db_ids) != 0:
        db_ids = db_ids.replace('\n','')
        db_set.add(db_ids)
        if db_ids not in emp_int:
            to_rem.add(db_ids)
        db_ids = f_db.readline()
    f_db.close()

    #print("DB employees: " + len (db_set).__str__())
    #print("Employees to inactivate: " + len(to_rem).__str__())

    
    #for emp_id in db_ids:
    #    if emp_id not in emp_int:
    #        to_rem.add(emp_id)
    #to_rem = db_set - emp_int
    
    print('<?xml version="1.0" ?><empload global_version="1.0">') 
    for emp_id in to_rem:
        print('<entry emp_cd="' + emp_id.__str__() + '" >')
        print('<status code="R" eff_date="04/3/2012"/></entry>')
        #print(emp_id)
    print('</empload>')