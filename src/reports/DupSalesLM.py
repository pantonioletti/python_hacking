from reports import PWMRepCommon
import sys



def dupSalesLM(connStr, output, org_cd, start_date, end_date):
    
    conn = PWMRepCommon.openConn(connStr)

    orgList = PWMRepCommon.getAllChildrenConn(conn, org_cd)

    calList = PWMRepCommon.getDaylyCalendar(conn, 1, start_date, end_date)
    toDel = list()
    del_str = "delete from budget_detail_import where org_entry_id = "
    for i in range(0, len(calList)):
        for j in range(0, len(orgList)):
            actualValue = PWMRepCommon.getBudgetActualValue(conn, orgList[j].id, 2, calList[i][0])
            if (len(actualValue) > 0):
                svalue = actualValue[0][0]
                salesLM = PWMRepCommon.getSalesLM(conn,orgList[j].id, 2, calList[i][1])
                if (len(salesLM) > 1):
                    rowid = -1
                    det_del_str = del_str + orgList[j].id.__str__() + " AND data_row_id IN ("
                    first_time = True
                    for k in range(0, len(salesLM)):
                        if (rowid == -1 and salesLM[k][1] == svalue):
                            rowid = salesLM[k][0]
                        else:
                            if (not first_time):
                                det_del_str = det_del_str + ","
                            else:
                                first_time = False
                            det_del_str = det_del_str + salesLM[k][0].__str__()
                    det_del_str = det_del_str + ");"
                    toDel.append(det_del_str)
    fd = open(output + "-" + org_cd + ".txt", 'a')
    for i in range(0, len(toDel)):
        fd.write(toDel[i])
        fd.write('\n')
    fd.close()

    return toDel