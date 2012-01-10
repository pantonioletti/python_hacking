import os
from reports.PWMRepCommon import buildConnStr
from reports.PWMRepCommon import openConn


''' 
    Indexa un diccionario por sus valores
    se debe tener en consideracion que valores
    repetidos generaran una sola entrada y el
    ultimo asignado queda
'''
def indexbyval(dic):
    newdic = dict()
    for k in dic.iterkeys():
        newdic[dic[k]] = k
    return newdic

'''
    Lee archivo en formato <key>=<value> creando
    un diccionarios indexado por las llaves
'''
def loadPropFile(output):
    dcode = None
    dval = None
    try:
        fd = open(output, 'r')
        str = fd.readline()
        dcode = dict()
        dval = dict()
        colisions = 0
        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.partition('=')
            if (vals[0] != str):
                dcode[vals[0]] = vals[2]
                if (vals[2] in dval):
                    print("!@#%$#!!! Dos codigos con mismo valor: \n")
                    print ("      ", vals)
                    print ("      ", dval[vals[2]],  " = ", vals[2])
                    colisions = colisions + 1
                dval[vals[2]] = vals[0]
            str = fd.readline()
        fd.close()
        print ("Se encontraron ", colisions, " descripciones repetidas")
    except IOError:
        print ("File ", output, " not found")
    return (dcode, dval)

def load_privileges(conn):
    priv_sql = "SELECT PRIVILEGE_ID, PRIVILEGE_CD, PRIVILEGE_NAME \
                FROM PRIVILEGE \
                WHERE PRIVILEGE_ID >= 100000"
    
    priv = conn.cursor()
    priv.execute(priv_sql)
    
    row = priv.fetchone()
    priv_dic = dict()

    while (row is not None):
        priv_dic[row[0]] = row[2]
        row = priv.fetchone()
    
    priv.close()
    return priv_dic
    

def update_privi(user, passwd, service, output, path_to_files):
    connstr = buildConnStr(user, passwd, service)
    conn = openConn(connstr)
    
    dic_list = loadPropFile(path_to_files + "/Common.properties")
    dic_es_list = loadPropFile(path_to_files + "/Common_es.properties")

    priv_in_db = load_privileges(conn)
    conn.close()
    
    fd = open(output, 'a')
    for priv in priv_in_db.iterkeys():
        tryagain = False
        key = None
        try:
            key = dic_list[1][priv_in_db[priv]]
        except KeyError:
            #print "Not found in english"
            tryagain = True
        if (tryagain):
            try:
                key = dic_es_list[1][priv_in_db[priv]]
                tryagain = False
            except KeyError:
                fd.write("/* ID: "+ priv.__str__() + " Value : -->"+ priv_in_db[priv]+ "<-- not found */")
                fd.write("\n")
                    
        if (not tryagain):
            print ("ID: ", priv, " Key : ", key, " Value : ", dic_es_list[0][key])
            fd.write( "update privilege set PRIVILEGE_NAME = '" + dic_es_list[0][key] + "' where PRIVILEGE_ID = " + priv.__str__() + ";")
            fd.write("\n")
            
    fd.close()