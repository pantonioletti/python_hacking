import dbaccess.common

def readusitem(params):
    conn = dbaccess.common.Connection(dbaccess.common.Constants.CXORA,params[0],params[1],params[2])
    conn.openConn()
    cur = conn.getCursor()
    
    cur.execute("select UMENU, UVAR, ULAN, UTECHSEQ, USEQ, UDESCR, UCOMMENT \
                from usitem")
    
    row = cur.fetchone()
    
    while(row is not None):
        xx = row[6].read()
        start = xx.find("<TITLE>")
        if (start > -1):
            end = xx.find("</TITLE>")
            if (end > -1):
                str = ""
                for idx in range ((start+7),end):
                    str = str + xx[idx]
                print str, '\n'
        row = cur.fetchone()
    cur.close()
    conn.close()
    