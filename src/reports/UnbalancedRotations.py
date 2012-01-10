import PWMRepCommon

def UnbalancedRotations(org_cd, connStr, sdate, edate, output):
    conn = PWMRepCommon.openConn(connStr)
    org = PWMRepCommon.getOrg(conn, org_cd)
    if (org is None):
        conn.close()
        return None
    rot = PWMRepCommon.getRotations(conn, org.id, sdate, edate)
    if rot is None or len(rot) == 0:
        conn.close()
        return None
    print ("Para cada rotacion obtener el balanceo")
    for j in range(len(rot)):
        PWMRepCommon.getRotBalanceStatus(conn, org.id, rot[j].id, sdate, rot[j].weeks)
        print ("Org id: ", org.id," Rotation id: ", rot[j].id)
