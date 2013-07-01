#coding=ISO_8859-1
'''
Created on Dec 21, 2009

@author: pantonio
'''

class org_group:
    def __init__(self):
        self.level = 0
        self.orgs = set()
        
def load_attr12_db(conn):
    sql = 'select oe.org_entry_id, oav.attribute_value, oe.org_level_id '
    sql += 'from org_entry oe, org_attribute_value oav '
    sql += 'where oav.org_entry_id = oe.org_entry_id '
    sql += 'and oav.attribute_id = 12'
    
    cursor = conn.cursor()
    cursor.execute(sql)
    data = cursor.fetchall()
    cursor.close()
    
    attr_12 = dict()
    for row in data:
        if row[1] not in attr_12:
            attr_12[row[1]] = org_group()
            attr_12[row[1]].level = row[2]
        attr_12[row[1]].orgs.add(row[0])

    return attr_12
    

def load_empty_org_groups(orgs):
    try:
        fd = open(orgs,'r')
        str = fd.readline()
        org_grps = dict()
        
        # 0: org group cd
        # 1: org group name
        # 2: org_level
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            org_grps[vals[0]]=(vals[1], vals[2])
            str = fd.readline()
        fd.close()
        org_grp_id = 2
        for grp in org_grps.keys():
            
            sql = "insert into org_group (ORG_GROUP_ID,ORG_GROUP_CD,ORG_GROUP_NAME,ORG_GROUP_DEF,AUDIT_DATE,AUDIT_EMP_ID) "
            sql += "values (" + org_grp_id.__str__()+" ,'" + grp + "', '" + org_grps[grp][0] + "','<OGD><ACT>Y</ACT><INACT>N</INACT><FIL><TYPE>1</TYPE></FIL><SEL><TYPE>2</TYPE><OL>"
            sql += org_grps[grp][1].__str__() + "</OL><RE>Y</RE><ATT><AID>12</AID><AO>EQ</AO><AV>"
            sql += org_grps[grp][1] + "</AV><AD>1</AD></ATT></SEL></OGD>',"
            sql += "to_date('1/1/2010','mm/dd/yyyy'),1);\n"
            org_grp_id += 1
            print(sql)
            #print(grp + ';' + org_grps[grp])
    except IOError:
        print ("File ", orgs, " not found")

def load_org_groups(orgs, attr_12):
    try:
        fd = open(orgs,'r')
        str = fd.readline()
        org_grps = dict()
        
        # 0: org group cd
        # 1: org group name
        # 2: att 12
        # 3: org level
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            #if vals[0] in attr_12:
            #    if attr_12[vals[0]].level != vals[2]:
            #        print("#@!&%*$ " + vals[0] + " in a different level than in attr12")
            if vals[0] not in org_grps:
                org_grps[vals[0]]=(vals[1], vals[2], vals[3])
            str = fd.readline()
        fd.close()
        org_grp_id = 2
        for grp in org_grps.keys():
#            sql = "update org_group set ORG_GROUP_DEF ='"
#            sql += "<OGD><ACT>Y</ACT><INACT>N</INACT><FIL><TYPE>1</TYPE></FIL><SEL><TYPE>2</TYPE><OL>"
#            sql += attr_12[org_grps[grp][1]].level.__str__() + "</OL><RE>Y</RE><ATT><AID>12</AID><AO>EQ</AO><AV>"
#            sql += org_grps[grp][1] + "</AV><AD>1</AD></ATT></SEL></OGD>' "
#            sql += "where ORG_GROUP_CD = '" + grp + "';"

            
            sql = "insert into org_group (ORG_GROUP_ID,ORG_GROUP_CD,ORG_GROUP_NAME,ORG_GROUP_DEF,AUDIT_DATE,AUDIT_EMP_ID) "
            sql += "values (" + org_grp_id.__str__()+" ,'" + grp + "', '" + org_grps[grp][0] + "','<OGD><ACT>Y</ACT><INACT>N</INACT><FIL><TYPE>1</TYPE></FIL><SEL><TYPE>2</TYPE><OL>"
            sql += attr_12[org_grps[grp][1]].level.__str__() + "</OL><RE>Y</RE><ATT><AID>12</AID><AO>EQ</AO><AV>"
            sql += org_grps[grp][1] + "</AV><AD>1</AD></ATT></SEL></OGD>',"
            sql += "to_date('1/6/2005','mm/dd/yyyy'),1);\n"
            if org_grps[grp][1] not in attr_12:
                print("-- Code " + grp + " not found!!")
            else:
                for orgs in attr_12[org_grps[grp][1]].orgs:
                    sql += "insert into org_group_org_entry (ORG_GROUP_ID,ORG_ENTRY_ID) "
                    sql += "values (" + org_grp_id.__str__() + "," + orgs.__str__() + ");\n"
            org_grp_id += 1
            print(sql)
            #print(grp + ';' + org_grps[grp])
    except IOError:
        print ("File ", orgs, " not found")
        
def load_attr_12(attr):
    try:
        fd = open(attr,'r')
        str = fd.readline()
        attr_12 = dict()
        
        # 0: ORG_ID
        # 1: attr 12
        # 2: org level
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            if vals[1] not in attr_12:
                attr_12[vals[1]] = org_group()
                attr_12[vals[1]].level = vals[2]
            else:
                if vals[2] != attr_12[vals[1]].level:
                    print("#@!&%*$ " + vals[1] + " in two levels") 
            attr_12[vals[1]].orgs.add(vals[0])
            str = fd.readline()
        fd.close()
        return attr_12
    except IOError:
        print ("File ", attr, " not found")
        return None
    
