#coding=ISO_8859-1
'''
Created on 10-09-2009
  Data as it comes from excel sheets:
            Code 0;Name 1;Level Name 2;Parent Org Code 3;Enable Biometrics 4;Charge to 5;
            Charge to Home Org 6;Address1 7;Address 2 8;City 9;State 10;Zipcode 11;Phone 1 12;Phone 2 13;
            Location Name 14;Time Zone 15;Midnight Rule 16;Scheduling Increment 17;Work Day Start Time 18;Work Week Start Day 19;

@author: pantonio
'''
org_level = dict()
org_level['Compañía'] = 'RE'
org_level['Zona'] = 'ZO'
org_level['Tienda'] = 'TD'
org_level['Unidad Económica'] = 'UE'
org_level['Departamento'] = 'DP'

class org_entry:
    def __init__(self):
        self.code = ""
        self.name = ""
        self.level_cd = ""
        self.parent_code = ""
        self.parent_level = ""
        self.charge_to = None
        #Charge to Home Org;
        self.address_1 = None
        self.address_2 = None
        self.city = ""
        self.state = ""
        self.zipcode = ""
        self.phone_1 = None
        self.phone_2 = None
        self.location_name = ""
        self.time_zone = None
        self.midnight_rule = None
        self.scheduling_increment = None
        self.work_day_start_time = None
        self.work_week_start_day = None
        self.eff_date = '03/01/2004'
        self.open_time='11:00'
        self.close_time='21:00'

    def print_insert_rel(self):
        str = 'union select \'INSERT INTO ORG_RELATION (PARENT_ORG_ID, CHILD_ORG_ID, EFF_DATE, END_DATE) VALUES (\'||oe2.org_entry_id||\',\''
        str += '|| oe.org_entry_id || \',TO_DATE(\'\'20040301 05:00:00\'\',\'\'yyyymmdd hh24:mi:ss\'\'), NULL);\' '
        str += 'from org_entry oe, org_entry oe2 '
        str += 'where oe.org_entry_cd = \'' + self.code + '\' '
        str += 'and oe2.org_entry_cd =\'' + self.parent_code + '\''
        print(str)

    def print_org(self, time, unit_org_level, any):
        str = '<entry '
        str += 'org_cd="' + self.code +'" '
        str += 'org_level_cd="' + self.level_cd + '" '
        str += 'name="' + self.name + '" '
        str += 'locationname="' + self.location_name + '" '
        if (self.city != ''):
            str += 'city="' + self.city + '" '
        if (self.state != ''):
            str += 'state="' + self.state + '" '
        if (self.zipcode != ''):
            str += 'zip="' + self.zipcode + '" '
        if (self.charge_to != ''):
            str += 'charge_labor="' + self.charge_to + '" '
        str += '>\n'
        str += '<status code="Active" eff_date="' + self.eff_date + '" />'
        str += '\n'
        if len(self.parent_code) > 0:
            str += '<orgrel '
            str += 'org_cd="' + self.parent_code + '" '
            str += 'org_level_cd="' + self.parent_level + '" '
            str += 'eff_date="' + self.eff_date + '" />'
            str += '\n'
        if time and self.level_cd == unit_org_level:
            str += '<hrs_pattern day_cd="Mon" eff_date="' + self.eff_date + '" open="Y" open_time="' + self.open_time + '" close_time="' + self.close_time + '" />'
            str += '\n' 
            str += '<hrs_pattern day_cd="Tue" eff_date="' + self.eff_date + '" open="Y" open_time="' + self.open_time + '" close_time="' + self.close_time + '" />'
            str += '\n' 
            str += '<hrs_pattern day_cd="Wed" eff_date="' + self.eff_date + '" open="Y" open_time="' + self.open_time + '" close_time="' + self.close_time + '" />'
            str += '\n' 
            str += '<hrs_pattern day_cd="Thu" eff_date="' + self.eff_date + '" open="Y" open_time="' + self.open_time + '" close_time="' + self.close_time + '" />'
            str += '\n' 
            str += '<hrs_pattern day_cd="Fri" eff_date="' + self.eff_date + '" open="Y" open_time="' + self.open_time + '" close_time="' + self.close_time + '" />'
            str += '\n' 
            str += '<hrs_pattern day_cd="Sat" eff_date="' + self.eff_date + '" open="Y" open_time="' + self.open_time + '" close_time="' + self.close_time + '" />'
            str += '\n' 
            str += '<hrs_pattern day_cd="Sun" eff_date="' + self.eff_date + '" open="Y" open_time="' + self.open_time + '" close_time="' + self.close_time + '" />'
            str += '\n' 
        str += any
        str += '</entry>'
        print(str)

class org_entry_small:
    def __init__(self):
        self.id = ""
        self.code = ""
        self.level_cd = ""
        self.name = ""
        self.location = ""
        self.positions = dict()
    def pprint(self):
        str = '<entry '
        str += 'org_cd="' + self.code +'" '
        str += 'org_level_cd="' + self.level_cd + '" '
        if len(self.name.strip())> 0:
            str += 'name="' + self.name + '" '
        if len(self.location.strip())> 0:
            str += 'locationname="' + self.location + '" >\n'
        for pos_key in self.positions.keys():
            if  len(self.positions[pos_key].name) > 32:
                self.positions[pos_key].name = self.positions[pos_key].name[0:32]
                str += '<!-- This postion name is too long -->'
            str += '<position code="' + self.positions[pos_key].code + '" name="' + self.positions[pos_key].name + '" >\n'
            str += '<position_status code="Active" eff_date="03/01/2004" />\n'
            if self.positions[pos_key].role is not None:
                str += '<position_role code="' + self.positions[pos_key].role + '" op_code="U" />\n'
            for act_key in self.positions[pos_key].activities.keys():
                str += '<position_activity code="' +self.positions[pos_key].activities[act_key].code + '" default_on="Y" op_code="U" />\n'
            for as_key in self.positions[pos_key].additional_scope.keys():
                str += '<position_scope_org org_cd="' +self.positions[pos_key].additional_scope[as_key].code + '" org_level_cd="' + self.positions[pos_key].additional_scope[as_key].level_cd + '" op_code="U" />\n'
                
            str += '</position>\n'
        str += '</entry>\n'
        print(str)
        
        
def load_org_entries(orgs, date, unit_org_level, d_org_pos):
    try:
        fd = open(orgs,'r')
        str = fd.readline()
        print('<?xml version="1.0" encoding="ISO_8859-1" ?>')
        print('<root>')

        #0:org_cd;
        #1:name;
        #2:org_level_cd ;
        #3:org_cd (parent);
        #4:org_level_cd (parent);
        #5:biometric;
        #6:charge_labor;
        #7: charge to home org
        #8: locationname
        #9: Time Zone
        #10: Midnight Rule
        #11: Scheduling Increment
        #12: Work Day Start Time
        #13: Work Week Start Day

        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            new_org = org_entry()
            new_org.code = vals[0]
            new_org.name = vals[1]
            new_org.level_cd = vals[2]
            new_org.eff_date = date
            if (new_org.level_cd is None):
                print("WARNING - Unknown org_level (3rd) data: =>" + str)
            new_org.parent_code = vals[3]
            new_org.parent_level = vals[4]
            new_org.charge_to = vals[6]
            new_org.location_name = vals[8]
            d_pos = d_org_pos.pop(new_org.code, None)
            s_pos = ""
            if d_pos is not None:
                for pos_key in d_pos.keys():
                    s_pos += d_pos[pos_key].print_pos() 
            new_org.print_org(True, unit_org_level, s_pos)
            #x=dict()
            str = fd.readline()
        print('</root>')
        fd.close()
    except IOError:
        print ("File ", orgs, " not found")

def load_positions(pos, d_act, date):
    d_org_pos = dict()
    try:
        fd = open(pos,'r')
        str = fd.readline()
        p_code = '_'
        o_code = '_'
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            #0: Code;
            #1: Position Name;
            #2: Org code;
            #3: Org name;
            #4: act code
            #5: act name;
            #6: Fixed (Y|N);
            #7: Roles
            if (p_code != vals[0] or o_code != vals[2]):
                new_pos = position()
                new_pos.code = vals[0]
                p_code = vals[0]
                o_code = vals[2]
                new_pos.name = vals[1]
                new_pos.role = vals[7]
                new_pos.status_eff_date = date
                if vals[2] not in d_org_pos:
                    d_org_pos[vals[2]]=dict()
                d_org_pos[vals[2]][vals[0]] = new_pos
            else:
                new_pos = d_org_pos[vals[2]][vals[0]]
            if vals[4] in d_act:
                new_pos.activities.append(vals[4])
            elif len(vals[4].strip())> 0:
                print("Activity not found: " + str)
            
            str = fd.readline()
        fd.close()
    except IOError:
        print ("File ", pos, " not found")
    return d_org_pos

def load_org_pos(orgs, pos):
    try:
        fd = open(orgs,'r')
        str = fd.readline()
        d_orgs = dict()
        #print('<?xml version="1.0" encoding="ISO_8859-1" ?>')
        #print('<root>')
        #0:org_cd;
        #1:name;
        #2:org_level_cd ;
        #3:org_cd (parent);
        #4:org_level_cd (parent);
        #5:biometric;
        #6:charge_labor;
        #7:city;
        #8:state;
        #9:zip;
        #10:locationname
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            if (vals[2] == 'DP' or vals[2] == 'UE'):
                new_org = org_entry()
                new_org.code = vals[0]
                new_org.name = vals[1]
                new_org.level_cd = vals[2]
                if (new_org.level_cd is None):
                    print("WARNING - Unknown org_level (3rd) data: =>" + str)
                new_org.parent_code = vals[3]
                new_org.parent_level = vals[4]
                new_org.charge_to = vals[6]
                new_org.city = vals[7]
                new_org.state = vals[8]
                new_org.zipcode = vals[9]
                new_org.location_name = vals[10]
                d_orgs[new_org.code] = new_org
            str = fd.readline()
        fd.close()

        fd = open(pos,'r')
        str = fd.readline()
        d_org_pos = dict()
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            #0: Code;
            #1: Position Name;
            #2: Org(s);
            #3: Org code;
            #4: Activities;
            #5: Código;
            #6: Tipo;
            #7: Fixed (Y|N);
            #8: Roles
            if (d_orgs.get(vals[3]) is not None):
                new_pos = position()
                new_pos.code = vals[0]
                new_pos.name = vals[1]
                new_pos.activities.add()
                if (d_org_pos.get(vals[3]) is None):
                    s_pos = set()
                    d_org_pos[vals[3]] = s_pos
                else:
                    s_pos = d_org_pos[vals[3]] 
                
            str = fd.readline()
        fd.close()
    except IOError:
        print ("File ", orgs, " not found")
        
class activity:
    def __init__(self):
        self.code = ""
        self.level = ""
        self.name = ""
        
class position:
    def __init__(self):
        self.code = ""
        self.name = ""
        self.status_code = "Active"
        self.status_eff_date = "03/01/2004"
        self.activities = list()
        self.charge_to_org_cd = ""
        self.charge_to_org_level = ""
        self.role = ""
        self.additional_scope = dict()
    
    def print_pos(self):
        str = '<position code="' + self.code + '" name="' + self.name + '" >\n'
        str += '<position_status code="Active" eff_date="' + self.status_eff_date + '" />\n'
        for i in range(len(self.activities)):
            str += '<position_activity code="' + self.activities[i].__str__() + '" default_on="Y" op_code="U" />\n'
        #str += '<position_charge_org org_cd="" org_level_cd="" />\n'
        str += '</position>\n'
        return str



def print_xml_org_positions(d_orgs):
    orgs = d_orgs.values()
    status = '<position_status code="Active" eff_date="03/01/2004" />\n'
    for o in orgs:
        if (len(o.positions) == 0):
            continue
        xml = '<entry org_cd="' + o.code + '" '
        xml += 'org_level_cd="' + o.level_cd + '" '
        xml += 'locationname="' + o.location + '" >\n'
        pos = o.positions.values()
        for p in pos:
            xml += '<position code="' + p.code + '" '
            xml += 'name="' + p.name + '" >\n'
            xml += status
            xml += '<position_charge_org org_cd="' + p.charge_to_org_cd + '" '
            xml += 'org_level_cd="' + p.charge_to_org_level + '" />\n'
            #xml += '<position_role code="' + p.role + '" op_code="U" />\n'
            act = p.activities.values()
            for a in act:
                xml += '<position_activity code="' + a.code + '" '
                xml += 'default_on="Y" op_code="U" />\n'
            xml += '</position>\n'
        xml += '</entry>'
        print(xml)
        


def load_org_positions(orgs, d_orgs):
    try:
        fd = open(orgs,'r')
        str = fd.readline()
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            #31000056;Vendedor;PEDP0040D113;DP;PEDP0040D113;DP;TRA-100018;TRAB;N;EMP
            #CLR051208;VENDEDOR PART TIME;B11;CLWG0057BELI;BELLEZA ISLAS;VTA-B11;Ventas - BELLEZA ISLAS;Dinamico;Trabajo;N;EMP
            # 0: Code
            # 1: Position Name
            # 2: Org level
            # 3: Org CD
            # 4: Code Activity
            # 5: Fixed (Y|N)
            # 6: Roles
            # 7: Addtiional scope org cdode
            # 8: Additional scope org level
            # 9: location name
            key = vals[3]
            if (key in d_orgs):
                org_entry = d_orgs[vals[3]]
            else:
                org_entry = org_entry_small()
                org_entry.code = vals[3]
                #org_entry.name = vals[3]
                org_entry.level_cd = vals[2]
                d_orgs[vals[3]] = org_entry
                if len(vals[9].strip())> 0:
                    org_entry.location = vals[9]    
            if vals[0] in org_entry.positions:
                org_pos = org_entry.positions[vals[0]]
            else:
                org_pos = position()
                org_pos.code = vals[0]
                org_pos.name = vals[1][0:32]
                if len(vals[6]) > 0:
                    org_pos.role = vals[6]
                else:
                    org_pos.role = None
                org_entry.positions[vals[0]]=org_pos
                
            if vals[4] not in org_pos.activities:
                act_entry = activity()
                act_entry.code = vals[4]
                org_pos.activities[vals[4]] = act_entry
            
                
            if len(vals[7].strip())> 0:
                addic_scope = org_entry_small()
                addic_scope.code = vals[7]
                addic_scope.level_cd = vals[8]
                org_pos.additional_scope[vals[7]] = addic_scope
            str = fd.readline()
        #print('</root>')
        fd.close()
        print('<?xml version="1.0" encoding="ISO_8859-1" ?>')
        print('<root>')
        for org_key in d_orgs.keys():
            #d_orgs[org_key].location = 'FLORIDA CENTER'
            d_orgs[org_key].pprint()
        print('</root>')
    except IOError:
        print ("File ", orgs, " not found")





def load_org_entries_db(orgs):
    d_orgs = dict()
    try:
        fd = open(orgs,'r')
        str = fd.readline()
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            #ol.org_level_cd,oe.org_entry_cd, oe.org_entry_name, oe.location_name
            if (vals[3] == 'Tienda Modelo'):
                new_org = org_entry_small()
                new_org.code = vals[1]
                new_org.level_cd = vals[0]
                new_org.location = vals[3]
                new_org.name = vals[2]
                level_code = vals[0]+'#'+vals[1]
                d_orgs[level_code] = new_org
            str = fd.readline()
        #print('</root>')
        fd.close()
    except IOError:
        print ("File ", orgs, " not found")
        d_orgs = None
    return d_orgs

def load_db_data_from_file(orgs):
    d_orgs = dict()
    try:
        fd = open(orgs,'r')
        str = fd.readline()
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            level_code = vals[0]+'#'+vals[1]
            name = vals[2]
            d_orgs[level_code] = name
            str = fd.readline()
        fd.close()
    except IOError:
        print ("File ", orgs, " not found")
        d_orgs = None
    #print(d_orgs)
    return d_orgs

def comp_name_to_db(orgs, db_data):
    try:
        fd = open(orgs,'r')
        str = fd.readline()
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            level_code = vals[0]+'#'+vals[1]
            name = vals[2]
            if (db_data[level_code] is None):
                print('This data does not match with anything:\n')
                print(str)
                print('\n')
            else:
                if (db_data[level_code] != name):
                    sql = "UPDATE ORG_ENTRY SET ORG_ENTRY_NAME = '" + name
                    sql += "' WHERE ORG_LEVEL_ID = " + vals[0]
                    sql += " AND ORG_ENTRY_CD = '" + vals[1] + "';"
                    print(sql)
            str = fd.readline()
        fd.close()
    except IOError:
        print ("File ", orgs, " not found")

def b_org_structure(orgs):
    try:
        fd = open(orgs,'r')
        str = fd.readline()
        d_orgs = dict()
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            #0:oe.org_entry_name, 
            #1:substr(oe.org_entry_cd,length(oe.org_entry_cd)-3,4), 
            #2:oe.org_level_id, 
            #3:orr.parent_org_id, 
            #4:orr.child_org_id            
            org_id = vals[4]
            new_org = org_entry_small()
            new_org.code = vals[1]
            new_org.name = vals[0]
            
            if (vals[2] == '4'):
                d_orgs[org_id] = new_org
            else:
                if (vals[3] in d_orgs):
                    parent = d_orgs[vals[3]]
                    parent.positions[org_id] = new_org
                else:
                    print('!!!!!A child without a parent!!!!!!: \n')
                    print(vals[1] + '#' + vals[0] + '#' + vals[3].__str__() + '#' + vals[4].__str__())
                        
            str = fd.readline()
        fd.close()
    except IOError:
        print ("File ", orgs, " not found")

    borg_id = 2
    uuid = 150
    ue_rank = 1
    for org in d_orgs.values():
        str = '            <subunit displayName="' + org.name + '" '
        str += 'borgID="' + borg_id.__str__() + '" '
        str += 'typeAttrVal="' + org.code + '" '
        str +=  'rank="' + ue_rank.__str__() + '" '
        str += 'orgtype="1" UUID="0_689_' + uuid.__str__() + '"'
        borg_id += 1
        uuid += 1
        ue_rank += 1
        if (len(org.positions) == 0):
            str += '/>\n'
        else:
            str += ' >\n'
            dp_rank = 1
            for child_org in org.positions.values():
                str += '                <subunit displayName="' + child_org.name +'" '
                str += 'borgID="' + borg_id.__str__() +'" '
                str += 'typeAttrVal="' + child_org.code + '" '
                str += 'rank="' + dp_rank.__str__() +'" '
                str += 'orgtype="1" UUID="0_689_' + uuid.__str__() + '" />\n'
                borg_id += 1
                uuid += 1
                dp_rank += 1
            str += '            </subunit>\n'
        print(str)

def strore_structure(org_st, org_level):
    fd = open(org_st,'r')
    str = fd.readline()
    d_orgs = dict()
    while(len(str) != 0):
        str = str.replace('\n', '')
        vals = str.rsplit(';')
        str = fd.readline()
        #Entry Code;
        #Entry Name;
        #Level code;
        #Parent Org Code;
        #Enable Biometrics;
        #Charge to;
        #Charge to Home Org;
        #Location Name;
        #Time Zone;
        #Time Zone Code;
        #Midnight Rule;
        #Midnight rule code;
        #Scheduling Increment;
        #Work Day Start Time;
        #Work Week Start Day;
        #Org group




#BOrgStructure.xml
#b_org_structure('C:/dev/projects/PWMPython/borgstructure.txt')
#BOrgStructure.xml
#Code;Position Name;code org;level;code charge org;level;Código;Tipo;Fixed (Y|N);Roles

#load_org_pos('C:/dev/projects/PWMPython/org_entries-Ripley.txt', 'C:/dev/projects/PWMPython/positions-Ripley.txt')
#comp_name_to_db('C:/dev/projects/PWMPython/org-Ripley-update-desc.txt', db_data)
#db_data = load_db_data_from_file('C:/dev/projects/PWMPython/org_entry_data.txt')

# POSITIONS
#db_data = load_org_entries_db('C:/dev/projects/ScriptsUtil/data/input/org_entry_data.txt')
#load_org_positions('C:/dev/projects/ScriptsUtil/data/input/positions-Ripley.txt', db_data)
#header = '<?xml version="1.0" encoding="ISO_8859-1" ?>\n'  
#header += '<!DOCTYPE orgapiload>\n'
#header += '<orgapiload global_version="1.0">\n'
#print(header) 
#print_xml_org_positions(db_data)
#print('</orgapiload>')
# POSITIONS
#LOAD ORG
#org_data = load_org_entries('C:/dev/projects/ScriptsUtil/data/input/orgs_trujillo.txt')
#LOAD ORG


#comp_name_to_db('C:/dev/projects/PWMPython/org-Ripley-update-desc.txt', db_data)