import dbaccess.common
import pmm.pmmentities

def getrejdata(connparams, rejcode):
    conn = dbaccess.common.Connection(dbaccess.common.Constants.CXORA,connparams[0], connparams[1],connparams[2])
    conn.openConn()
    cur = conn.getCursor()
    cur.execute("select unique ir.trans_prd_child \
    from invrejee ir \
    where ir.error_code = " + rejcode.__str__())
    row = cur.fetchone()
    while(row is not None):
        #print(row)
        inners = getinnerpackcod(connparams, row[0])
        if (inners is None):
            print("What the hell ", row[0], " has no inner pack.\n")
        elif (len(inners)==1):
            curu = conn.getCursor()
            curu.execute("update invrejee \
            set inner_pk_tech_key = " + inners[0].__str__() + "\
            where trans_prd_child = " + row[0].__str__() + "\
            and error_code = " + rejcode.__str__())
            print("prd_lvl_child ", row[0], " updated")
            #print(" and its inner pack code is ", inners[0])
        row = cur.fetchone()
    cur.close()
    conn.commit()
    conn.close()

def getinnerpackcod(connparams, prdlvlchild):
    conn = dbaccess.common.Connection(dbaccess.common.Constants.CXORA,connparams[0], connparams[1],connparams[2])
    conn.openConn()
    cur = conn.getCursor()
    cur.execute("select pd.inner_pk_tech_key \
                from prdpcdee pd \
                where pd.prd_lvl_child = " + prdlvlchild.__str__())
    inners = list()
    row = cur.fetchone()
    while(row is not None):
        print(row)
        inners.extend(row)
        row = cur.fetchone()
        
    cur.close()
    conn.close()
    return inners


def getpodata():
    conn = dbaccess.common.Connection(dbaccess.common.Constants.CXORA,"jdapmmds", "jdapmmds","DYS_DESA")
    conn.openConn()
    cur = conn.getCursor()
    cur.execute("select sysdate from dual")
    row = cur.fetchone()
    print(row)
    cur.close()
    conn.close()

def getinvoicedata():
    conn = dbaccess.common.Connection(dbaccess.common.Constants.CXORA,"jdapmmds", "jdapmmds","DYS_DESA")
    conn.openConn()
    cur = conn.getCursor()
    cur.execute("select * from chlcexee")
    row = cur.fetchone()
    while(row is not None):
        print(row)
        row = cur.fetchone()
    cur.close()
    conn.close()
def test1028(connprams):
    conn = dbaccess.common.Connection(dbaccess.common.Constants.CXORA,connprams[0], \
                                        connprams[1], connprams[2])
    conn.openConn()
    gdheader = pmm.pmmentities.getGDHdr(conn, connprams[3])
    gdheader.setDetail(pmm.pmmentities.getGDDet(conn,gdheader.inv_mov_tech_key))
    for i in range(0, len(gdheader.detail)):
        gdheader.detail[i].setTaxes(pmm.pmmentities.getGDTaxes(conn,gdheader.inv_mov_tech_key,\
                            gdheader.detail[i].seq_num, gdheader.detail[i].prd_lvl_child))
    conn.close()
def val_rtv_doc(rtv_number):
    conn = dbaccess.common.Connection(dbaccess.common.Constants.CXORA,"jdapmmds", "jdapmmds","DYS_DESA")
    conn.openConn()
    cur = conn.getCursor()
    str_sql = "SELECT PRD_LVL_CHILD, RTV_QTY_SHIP, RTV_UNIT_COST, RTV_SHIP_DATE, PRD_UPC, RTV_UNIT_TAX \
                RTV_SELL_PER_INNER, RTV_NUMBER_OF_INNERS, RTV_ENTRY_METHOD \
                FROM rtvdtlee d WHERE d.rtv_number = " + rtv_number.__str__()
    cur.execute(str_sql)
    
    row = cur.fetchone()
    while (row is not None):
        entry_method = row[8]
        units = None
        cost = None
        factor = None
        if (entry_metthod == 1):
            # unidades
            print( "Unidades")
            factor = 1
        elif (entry_metthod == 2):
            # Case pack
            print( "Case pack")
            factor = row[6]*row[7]
        elif (entry_metthod == 3):
            # inner pack
            print( "Inner pack")
            factor = row[6]
        elif (entry_metthod == 4):
            # GTIN de producto
            print( "GTIN de producto")
        elif (entry_metthod == 5):
            # GTIN de case pack
            print( "GTIN de case pack")
        else:
            print( "Algo esta mal")
        units = row[1] * factor
        cost = row[2] / factor
        row = cur.fetchone()
    cur.close()
    conn.close()
    
