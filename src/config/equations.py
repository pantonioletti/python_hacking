#coding=ISO_8859-1
'''
Created on Nov 17, 2009

@author: pantonio
'''
import sys
def parse_equation(eq):
    eq = eq.replace(' ', '')
    op = eq.count('(')
    cl = eq.count(')')

    if (op != cl):
        raise Exception("Open-close parenthesis mismatch")
    
    l_eq_var = list()
    staff_var = ''
    symbols = ['(',')','+','-','*','/']
    var_num = 1
    new_eq = ''
    for i in range(len(eq)):
        if (eq[i] in symbols):
            if (len(staff_var.strip()) > 0):
                staff_var = staff_var.strip()
                if not staff_var.isnumeric():
                    l_eq_var.append(staff_var)
                    new_eq += staff_var + '_' + var_num.__str__()
                    var_num += 1
                else:
                    new_eq += staff_var 
            staff_var = ''
            new_eq += eq[i]
        else:
            staff_var += eq[i]
    if len(staff_var.strip()) > 0:
        if not staff_var.isnumeric():
            l_eq_var.append(staff_var)
            new_eq += staff_var + '_' + var_num.__str__()
        else:
            new_eq += staff_var
    return (l_eq_var, new_eq) 

def load_equations(file,conn):
    '''
    paso 1: insertar staffing_variable
    paso 2: insertar en staffing_equation (luego de actualizar archivo staffing_variable.txt
    paso 3: insertar en staffing_equation_variable
    paso 4: insertar en staffing_equation_activity
    ''' 
    try:
        fd = open(file, 'r')
        str = fd.readline()
        count = 0
        #err_vars = set()
        err_eqs = dict()
        cursor = conn.cursor()
        
        #Step 1: load staffing variables
        sql = "select staffing_variable_cd, staffing_variable_id from  staffing_variable where staffing_variable_type_id <> 1"
        cursor.execute(sql)
        rows = cursor.fetchall()
        var_cd_id = dict()
        for one_row in rows:
            var_cd_id[one_row[0]] = one_row[1]
            
        #Step 2: load activities
        sql = "select ae.activity_entry_cd, ae.activity_entry_id from activity_entry ae"
        cursor.execute(sql)
        rows = cursor.fetchall()
        act_cd_id = dict()
        for one_row in rows:
            act_cd_id[one_row[0]] = one_row[1]
        
        # 0: código ecuación
        # 1: Nombre ecuación
        # 2: Código actividad asociada
        # 3: Tipo (MINUTOS)
        # 4: Ecuación 
        # 5: Org
        # 6: Min Max (Y|N)
        while(len(str) != 0):
            count += 1
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            ok = True
            parse_ret = ([], [])
            err_eqs[vals[0]] = list()

            #if vals[0] == 'VENTA309':
            #    pass
            if len(vals[2].strip()) > 0 and vals[2] not in act_cd_id:
                print('Activity error in equation ' + vals[0])
                ok = False
            else:
                #if vals[0] == 'TraAssrSDC':
                #    pass
                if len(vals[4]) > 0:#len(vals) == 4:
                    try:
                        parse_ret = parse_equation(vals[4])
                    except Exception as exc:
                        err_eqs[vals[0]].append("Equation error " + exc.args[0])
                        ok = False
                    if ok :
                        for var_cd in parse_ret[0]:
                            if var_cd not in var_cd_id:
                                err_eqs[vals[0]].append("Equation " + vals[0] + " error")
                                err_eqs[vals[0]].append("Variable " + var_cd + " does not exist")
                                ok = False
                if ok:
                    # Insert staffing variable
                    try:
                        cursor.execute('select SEQ_STAFFING_VARIABLE_ID.nextval from dual')
                        r = cursor.fetchone()
                        sv_id = r[0]
                        sql = "INSERT INTO staffing_variable "
                        sql += "(staffing_variable_id, staffing_variable_cd, staffing_variable_name, format_string, sum_p, uom_id, staffing_variable_type_id, productivity_p) "
                        sql += "VALUES (" + sv_id.__str__() + ", '" + vals[0] + "', '" + vals[1][0:32] + "', NULL, NULL, 2, 1, 0)"
                        cursor.execute(sql)
                        
                        cursor.execute('select SEQ_EQUATION_ID.nextval from dual')
                        r = cursor.fetchone()
                        se_id  = r[0]
                        if len(vals[4]) > 0:
                            eq_val = parse_ret[1] #vals[3].replace(' ', '')
                        else:
                            eq_val = 'equationforstaffingvariableid' + sv_id.__str__()
                            
                        sql = "INSERT INTO staffing_equation (equation_id, equation, staffing_variable_id) VALUES "
                        sql += "(" + se_id.__str__() + ",'" +eq_val+ "' ," + sv_id.__str__() + ")"
                        cursor.execute(sql)
                        
                        if len(vals[2].strip()) > 0:
                            cursor.execute('select SEQ_EQUATION_LINK_ID.nextval from dual')
                            r = cursor.fetchone()
                            el_id = r[0]
                            sql = "INSERT INTO staffing_equation_activity (equation_link_id, calculate_increment, equation_id, activity_entry_id, org_entry_id, strictly_org_hours_p) "
                            sql += "VALUES (" + el_id.__str__() + ", 15," + se_id.__str__() + " , " + act_cd_id[vals[2]].__str__() + ", NULL, 'N')"
                            cursor.execute(sql)
    
                        min_max_ids = list()
                        sql = ""
                        cursor.execute('select SEQ_EQUATION_VARIABLE_ID.nextval from dual')
                        r = cursor.fetchone()
                        ev_id = r[0]
                        sql = "INSERT INTO staffing_equation_variable (equation_variable_id, counter, staffing_variable_id, equation_id) "
                        sql += "VALUES (" + ev_id.__str__() + ", -1, 1, " + se_id.__str__() + ")"
                        cursor.execute(sql)
                        min_max_ids.append(ev_id)
                        
                        cursor.execute('select SEQ_EQUATION_VARIABLE_ID.nextval from dual')
                        r = cursor.fetchone()
                        ev_id = r[0]
                        sql = "INSERT INTO staffing_equation_variable (equation_variable_id, counter, staffing_variable_id, equation_id) "
                        sql += "VALUES (" + ev_id.__str__() + ", -1, 2, " + se_id.__str__() + ")"
                        cursor.execute(sql)
                        min_max_ids.append(ev_id)
                        
                        cursor.execute('select SEQ_EQUATION_VARIABLE_ID.nextval from dual')
                        r = cursor.fetchone()
                        ev_id = r[0]
                        sql = "INSERT INTO staffing_equation_variable (equation_variable_id, counter, staffing_variable_id, equation_id) "
                        sql += "VALUES (" + ev_id.__str__() + ", -1, 3, " + se_id.__str__() + ")"
                        cursor.execute(sql)
                        
                        counter = 1
                        for idx in range(len(parse_ret[0])):
                            v = parse_ret[0][idx]
                            cursor.execute('select SEQ_EQUATION_VARIABLE_ID.nextval from dual')
                            r = cursor.fetchone()
                            ev_id = r[0]
                            sql = "INSERT INTO staffing_equation_variable (equation_variable_id, counter, staffing_variable_id, equation_id) "
                            sql += "VALUES(" + ev_id.__str__() + "," + counter.__str__() + " , " + var_cd_id[v].__str__() + ", " + se_id.__str__() + ")"
                            counter += 1
                            cursor.execute(sql)
                            
                        #Mínimo y maximo
                        if vals[6] == 'Y': 
                            cursor.execute('select SEQ_EQUATION_VALUE_ID.nextval from dual')
                            r = cursor.fetchone()
                            eval_id = r[0]
                            sql = "insert into staffing_variable_value (EQUATION_VALUE_ID,EFF_SDATE,END_SDATE, "
                            sql += "EQUATION_VALUE,EQUATION_VALUE_DETAIL,EQUATION_VARIABLE_ID,ORG_ENTRY_ID, "
                            sql += "ACTIVITY_ENTRY_ID,STAFFING_VARIABLE_ID,ORG_GROUP_ID,ORG_GROUP_TAG) "
                            sql += "values (" + eval_id.__str__() + ", '20040301', NULL,0.0, '1,1,1,2|15,3|15,1,2,1,2|15,3|15,1,3,1,2|15,3|15,1,4,1,2|15,3|15,1,5,1,2|15,3|15,1,6,1,2|15,3|15,1,7,1,2|15,3|15,1',"
                            sql +=  min_max_ids[0].__str__() + ", 1, NULL, NULL, NULL, NULL)"
                            
                            cursor.execute(sql)

                            cursor.execute('select SEQ_EQUATION_VALUE_ID.nextval from dual')
                            r = cursor.fetchone()
                            eval_id = r[0]
                            sql = "insert into staffing_variable_value (EQUATION_VALUE_ID,EFF_SDATE,END_SDATE, "
                            sql += "EQUATION_VALUE,EQUATION_VALUE_DETAIL,EQUATION_VARIABLE_ID,ORG_ENTRY_ID, "
                            sql += "ACTIVITY_ENTRY_ID,STAFFING_VARIABLE_ID,ORG_GROUP_ID,ORG_GROUP_TAG) "
                            sql += "values (" + eval_id.__str__() + ", '20040301', NULL,0.0, NULL,"
                            sql +=  min_max_ids[1].__str__() + ", 1, NULL, NULL, NULL, NULL)"
                            
                            cursor.execute(sql)
                        print("Equation : " + vals[0] + " " + vals[1] + " added.")
                        var_cd_id[vals[0]] = sv_id
                    except KeyError:
                        print("rolling back")
                        raise
                    except Exception:
                        print("Error: " + sql)
                        raise
            if len(err_eqs[vals[0]]) == 0:
                err_eqs.pop(vals[0])
            str = fd.readline()
        fd.close()
        print(count.__str__() + ' lines processed')
        for err_key in err_eqs.keys():
            print("Equation : " + err_key)
            for msg in err_eqs[err_key]:
                print(msg)
            print()
        if len(err_eqs) > 0:
            for err_key in err_eqs.keys():
                for msg in err_eqs[err_key]:
                    print(err_key + " " + msg)
            raise Exception("Errores!!!!!!")
    except IOError:
        print ("File ", file, " not found")
    return None    

def load_ids(file):
    d_var = dict()
    try:
        fd = open(file, 'r')
        str = fd.readline()
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            d_var[vals[0]]=vals[1]
            str = fd.readline()
        fd.close()
    except IOError:
        print ("File ", file, " not found")
    return d_var    

def load_ae_ids(file):
    try:
        fd = open(file, 'r')
        str = fd.readline()
        d_var = dict()
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            d_var[vals[1]]=[vals[0],vals[2],]
            str = fd.readline()
        fd.close()
    except IOError:
        print ("File ", file, " not found")
    return d_var    

def load_var_el_grp(file, d_def, d_elem, d_grp):
    try:
        fd = open(file, 'r')
        str = fd.readline()
        # 0 : cod parametro
        # 1 : nombre parametro 
        # 2 : cod grupo
        # 3 : cod element
        # 4 : cod definicion
        d_vars = dict()
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            if vals[2] not in d_grp:
                print("Group not found in: " + str)
            elif vals[3] not in d_elem:
                print("Element not found in: " + str)
            elif vals[4] not in d_def:
                print("Definition not found in: " + str)
            else:
                d_vars[vals[0]]= [vals[1][:32],d_grp[vals[2]],d_elem[vals[3]],d_def[vals[4]],]
            str = fd.readline()
        fd.close()
    except IOError:
        print ("File ", file, " not found")
    return d_vars    

def insert_staff_vars(data, conn):

    cursor = conn.cursor()

    try:
        for key in data.keys():
            sql = "SELECT SEQ_STAFFING_VARIABLE_ID.NEXTVAL FROM DUAL"
            cursor.execute(sql)
            row = cursor.fetchone()
            sv_id = int(row[0])

            sql = "INSERT INTO staffing_variable " 
            sql += "(staffing_variable_id, staffing_variable_cd, staffing_variable_name, format_string, sum_p, uom_id, staffing_variable_type_id, productivity_p) "
            sql += "VALUES (" + sv_id.__str__() + ", '" + key + "', '" + data[key][0] + "', NULL, NULL, 5,2, 'N')"
            # Execute sql against DB
            cursor.execute(sql)

            sql = "insert into forecast_staffing_link (STAFFING_VARIABLE_ID,FORECAST_GROUP_ID,FORECAST_ELEMENT_ID,FORECAST_DEF_ID,LEAD_OR_LAG,STAFFING_INCREMENT) "
            sql += "values (" + sv_id.__str__() + ", " + data[key][1].__str__() + ", "
            sql += data[key][2].__str__() + ", " + data[key][3].__str__() + ", 0, 0)"
            
            cursor.execute(sql)
            
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    cursor.close()
    
def work_stds(file):
    try:
        fd = open(file, 'r')
        str = fd.readline()
        line = '<?xml version="1.0" encoding="ISO_8859-1" ?>\n'
        line += '<!DOCTYPE laborstdsload >\n'
        line += '<laborstdsload global_version="1.0">\n' 
        print(line)
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            #oTordenD308;Tiempo en Orde-CALZADO MUJER MAS;MINUTES;0.833
            #0: CODE oTordenmD101;
            #1: NAME T.Orden Acc. Muj.;
            #2: UOM MINUTES;
            #3: ORG PERERIPL0002;
            #4: VALUE 0.2;
            #5: EFFDATE 1/1/2000;
            line = '    <parameter code="' + vals[0] + '" name="' + vals[1] + '" uom="' + vals[2] + '">\n' 
            if len(vals[0]) > 12:
                line += '<!-- Parameter code ' + vals[0] + ' too long -->\n' 
            line += '        <value org_code="' + vals[3] + '" base_value="' + vals[4] + '" eff_date="03/01/2004" exp_date="01/01/2999" />\n'  
            line += '    </parameter>\n'
            print(line)
            str = fd.readline()
        print('</laborstdsload>\n')
         
        fd.close()
    except IOError:
        print ("File ", file, " not found")
    return None    

class work_standard:
    def __init__(self, code, name, type, value):
        self.code = code
        self.name = name
        self.type = type
        self.value = value
        self.org_ids = set()
        self.org_grps = set()
        self.id = 0
        
def insert_work_standards(org_groups, f_ws, uom, conn, org_entries):
    # 0: TOTALPRODUCT; code
    # 1: Productividad Total; name
    # 2: PERCENT; type
    # 3: 1; org code
    # 4: Falabella Corporate; org name
    # 5: ; group code
    # 6: ; group name
    # 7: 80.000; value
    fd = open(f_ws, 'r')
    str = fd.readline()
    d_w_std = dict()
    while(len(str) != 0):
        str = str.replace('\n', '')
        vals = str.rsplit(';')
        ws = None
        if vals[2] in uom:
            if vals[0] in d_w_std:
                ws = d_w_std[vals[0]]
            else:
                ws = work_standard(vals[0], vals[1], uom[vals[2]], float(vals[7]))
            if len(vals[3])> 0:
                if vals[3] in org_entries:
                    cvp=(int(org_entries[vals[3]]),float(vals[7]),)
                    ws.org_ids.add(cvp)
                else:
                    ws = None
                    print("Wrong org entry: " + vals[3].__str__())
            else:
                if len(vals[5]) > 0:
                    if vals[5] in org_groups:
                        cvp = (int(org_groups[vals[5]]),float(vals[7]),)
                        ws.org_grps.add(cvp)
                    else:
                        ws = None
                        print("Org group does not exist: " + vals[5].__str__())
                else:
                    ws = None
                    print("Neither org entry nor org group found: \n" + str)
        else:
            ws = None
            print("Wrong unit of mesure: " + vals[2].__str__())
        if ws  is not None:
            if ws.code not in d_w_std:
                d_w_std[ws.code] = ws
        str = fd.readline()
  

    try:
        cursor = conn.cursor()
        for param_cd in d_w_std.keys():
            
            sql = "SELECT SEQ_STAFFING_VARIABLE_ID.NEXTVAL FROM DUAL"
            cursor.execute(sql)
            row = cursor.fetchone()
            sv_id = int(row[0])
            
            sql = "INSERT INTO staffing_variable "
            sql += "(staffing_variable_id, staffing_variable_cd, staffing_variable_name, format_string, "
            sql += "sum_p, uom_id, staffing_variable_type_id, productivity_p) "
            sql += "VALUES (" + sv_id.__str__() + ", '" + d_w_std[param_cd].code + "', '" + d_w_std[param_cd].name 
            sql += "', NULL, NULL, " + d_w_std[param_cd].type.__str__() + ", 7, 'N')"
            
            cursor.execute(sql)

            it_orgs = iter(d_w_std[param_cd].org_ids)
            for org_id in it_orgs:
                sql = "SELECT SEQ_EQUATION_VALUE_ID.NEXTVAL FROM DUAL"
                cursor.execute(sql)
                row = cursor.fetchone()
                svv_id = int(row[0])
                
                sql = "INSERT INTO staffing_variable_value "
                sql += "(equation_value_id, eff_sdate, end_sdate, equation_value, equation_value_detail, equation_variable_id, "
                sql += "org_entry_id, activity_entry_id, staffing_variable_id, org_group_id) "
                sql += "VALUES (" + svv_id.__str__() + ", '20040101', NULL, " + org_id[1].__str__() #d_w_std[param_cd].value.__str__() 
                sql += ", NULL, NULL, " + org_id[0].__str__() + ", NULL, " + sv_id.__str__() + ", NULL)"
                
                cursor.execute(sql)

            it_grps = iter(d_w_std[param_cd].org_grps)
            for grp_id in it_grps:
                sql = "SELECT SEQ_EQUATION_VALUE_ID.NEXTVAL FROM DUAL"
                cursor.execute(sql)
                row = cursor.fetchone()
                svv_id = int(row[0])
                
                sql = "INSERT INTO staffing_variable_value "
                sql += "(equation_value_id, eff_sdate, end_sdate, equation_value, equation_value_detail, equation_variable_id, "
                sql += "org_entry_id, activity_entry_id, staffing_variable_id, org_group_id) "
                sql += "VALUES (" + svv_id.__str__() + ", '20040101', NULL, " + grp_id[1].__str__() #d_w_std[param_cd].value.__str__() 
                sql += ", NULL, NULL, NULL, NULL, " + sv_id.__str__() + ", " + grp_id[0].__str__() + ")"

                cursor.execute(sql)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    cursor.close()
    pass