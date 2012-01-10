from dbaccess.common import *

'''
   Retorna todas las cabeceras de devoluciones realizadas por el local
   "shiploc"
'''
def getRtvHeaders(conn, shiploc):
    
    strsql = "SELECT RTV_NUMBER, RTV_SHIP_LOC, VPC_TECH_KEY, VPC_SHP_POINT,\
RTV_ENTRY_DATE, RTV_APROV_DATE, RTV_AUTH_DATE, RTV_RLS_PICK_DATE, \
RTV_PICK_DATE, RTV_SHIP_DATE, RTV_CLOSE_DATE, RTV_TYPE_ID, \
TRF_CAR_ID, RTV_STATUS, RTV_NOTES, RTV_AUTH_NUMBER, \
RTV_CANCEL_DATE, RTV_REF_NUMBER, REQUESTED_BY \
FROM RTVHDREE WHERE RTV_SHIP_LOC IN (SELECT ORG_LVL_CHILD FROM ORGMSTEE \
WHERE ORG_LVL_NUMBER = " + shiploc.__str__() + ") \
AND RTV_NUMBER NOT IN (SELECT INV_MOV_NUMBER \
FROM CHLHDTEE \
WHERE INV_MOV_TYPE = 'D')"
    cur = conn.getCursor()
    cur.execute(strsql)
    row = cur.fetchone()
    data = list()
    while(row is not None):
        data.append(Rtvhdree(row))
        row = cur.fetchone()
    cur.close()
    return data
   
'''
   Retorna la cabecera de devolucion realizada por el local
   "shiploc", con numero "rtvnumber"
'''
def getRtvHeader(conn, shiploc, rtvnumber):
    
    strsql = "SELECT RTV_NUMBER, RTV_SHIP_LOC, VPC_TECH_KEY, VPC_SHP_POINT,\
RTV_ENTRY_DATE, RTV_APROV_DATE, RTV_AUTH_DATE, RTV_RLS_PICK_DATE, \
RTV_PICK_DATE, RTV_SHIP_DATE, RTV_CLOSE_DATE, RTV_TYPE_ID, \
TRF_CAR_ID, RTV_STATUS, RTV_NOTES, RTV_AUTH_NUMBER, \
RTV_CANCEL_DATE, RTV_REF_NUMBER, REQUESTED_BY \
FROM RTVHDREE WHERE RTV_SHIP_LOC IN (SELECT ORG_LVL_CHILD FROM ORGMSTEE \
WHERE ORG_LVL_NUMBER = " + shiploc.__str__() + ") \
AND RTV_NUMBER = " + rtvnumber.__str__() + "\
FROM CHLHDTEE \
WHERE INV_MOV_TYPE = 'D')"
    cur = conn.getCursor()
    cur.execute(strsql)
    row = cur.fetchone()
    data = None
    if(row is not None):
        data = Rtvhdree(row)
    cur.close()
    return data

class Rtvhdree:
    def __init__(self, data):
        self.rtv_number=data[0]
        self.rtv_ship_loc=data[1]
        self.vpc_tech_key=data[2]
        self.vpc_shp_point=data[3]
        self.rtv_entry_date=data[4]
        self.rtv_aprov_date=data[5]
        self.rtv_auth_date=data[6]
        self.rtv_rls_pick_date=data[7]
        self.rtv_pick_date=data[8]
        self.rtv_ship_date=data[9]
        self.rtv_close_date=data[10]
        self.rtv_type_id=data[11]
        self.trf_car_id=data[12]
        self.rtv_status=data[13]
        self.rtv_notes=data[14]
        self.rtv_auth_number=data[15]
        self.rtv_cancel_date=data[16]
        self.rtv_ref_number=data[17]
        self.requested_by=data[18]

'''
    Retorna datos de encabezado de guia de despacho
'''
def getRtvDet(conn, rtvnumber):
    strsql = "SELECT RTV_DTL_TECH_KEY, RTV_NUMBER, PRD_LVL_CHILD, RTV_SHP_LOC, \
VPC_TECH_KEY, RTV_QTY_REQ, VPC_SHP_POINT, RTV_QTY_APROV, \
RTV_QTY_AUTH, RTV_QTY_PICK, RTV_QTY_SHIP, RTV_QTY_CNCL, \
RTV_UNIT_COST, RTV_REF_NUMBER, RTV_SOURCE_ID, RTV_IN_CARTON, \
RTV_IN_MANIFEST, RTV_SHP_CARTON, RTV_SHP_MANIFEST, RTV_STATUS, \
RTV_TYPE_ID, RTV_PRIOR_ID, RTV_PICK_DATE, RTV_SHIP_DATE, \
RTV_CLOSE_DATE, RTV_DTL_NOTES, RTV_CANCEL_DATE, PRD_UPC, \
RTV_UNIT_TAX, VPC_PRD_TECH_KEY, INNER_PK_TECH_KEY, RTV_SELL_PER_INNER, \
RTV_NUMBER_OF_INNERS, RTV_QTY_UOM, RTV_WEIGHT, RTV_WEIGHT_UOM, \
RTV_ENTRY_METHOD, RTV_EACHES_PER_INNER, RTV_CURR_CODE \
FROM RTVDTLEE WHERE RTV_NUMBER " + rtvnumber.__str__()

def getGDHdr(conn, gdnumber):
    strsql = "SELECT INV_MOV_TECH_KEY, INV_MOV_TYPE, INV_MOV_NUMBER, INV_MOV_PAGE, \
DOC_NUMBER, DOC_STATUS, ORG_LVL_CHILD, PRINT_DATE, TARGET_NAME, \
TARGET_BAS_ADDR_1, TARGET_BAS_ADDR_2, TARGET_CITY, TARGET_RUT, \
TARGET_RUTDV, CARRIER_NAME, DRIVER_NAME, DRIVER_RUT, \
DRIVER_RUTDV, VEHICLE_PLATE, NOTES, DOWNLOAD_DATE, \
DOWNLOAD_DATE_2, TARGET_PHONE, PRINT_SYSDATE, PACKING_TYPE, \
PACKING_NUMBER, CODIGO_EXT, NUM_BOLETA, SLS_LOC_NUMBER, \
DOC_NUMBER_OLD, PACKING_KEY, REC_LOC_CHILD, TARGET_BAS_ADDR_3, \
TARGET_BAS_STATE, DOC_IDENTIDAD, TIPO_C_PAGO, NUM_C_PAGO, \
ORI_NAME, ORI_RUT, ORI_RUTDV, ORI_BAS_ADDR_1, \
ORI_BAS_ADDR_2, ORI_BAS_ADDR_3, ORI_BAS_CITY, ORI_BAS_STATE, \
UT_MARCA_PLACA, UT_CERTIFICADO, UT_LICENCIA, CHL_HET_RUT, \
CHL_HET_RUTDV, COD_CAUSA, TYPE_DOC_IDENTIDAD, TARGET_GIRO, \
DOC_REVERSE, IMP_ID, SOURCE_GIRO, DTE_CODE FROM CHLHDTEE \
WHERE DOC_NUMBER = " + gdnumber.__str__()
    cur = conn.getCursor()
    cur.execute(strsql)
    row = cur.fetchone()
    data = None
    if(row is not None):
        data = Chlhdtee(row)
    cur.close()
    return data


class Chlhdtee:
    def __init__(self, row):
        self.inv_mov_tech_key= row[0]
        self.inv_mov_type= row[1]
        self.inv_mov_number= row[2]
        self.inv_mov_page= row[3]
        self.doc_number= row[4]
        self.doc_status= row[5]
        self.org_lvl_child= row[6]
        self.print_date= row[7]
        self.target_name= row[8]
        self.target_bas_addr_1= row[9]
        self.target_bas_addr_2= row[10]
        self.target_city= row[11]
        self.target_rut= row[12]
        self.target_rutdv= row[13]
        self.carrier_name= row[14]
        self.driver_name= row[15]
        self.driver_rut= row[16]
        self.driver_rutdv= row[17]
        self.vehicle_plate= row[18]
        self.notes= row[19]
        self.download_date= row[20]
        self.download_date_2= row[21]
        self.target_phone= row[22]
        self.print_sysdate= row[23]
        self.packing_type= row[24]
        self.packing_number= row[25]
        self.codigo_ext= row[26]
        self.num_boleta= row[27]
        self.sls_loc_number= row[28]
        self.doc_number_old= row[29]
        self.packing_key= row[30]
        self.rec_loc_child= row[31]
        self.target_bas_addr_3= row[32]
        self.target_bas_state= row[33]
        self.doc_identidad= row[34]
        self.tipo_c_pago= row[35]
        self.num_c_pago= row[36]
        self.ori_name= row[37]
        self.ori_rut= row[38]
        self.ori_rutdv= row[39]
        self.ori_bas_addr_1= row[40]
        self.ori_bas_addr_2= row[41]
        self.ori_bas_addr_3= row[42]
        self.ori_bas_city= row[43]
        self.ori_bas_state= row[44]
        self.ut_marca_placa= row[45]
        self.ut_certificado= row[46]
        self.ut_licencia= row[47]
        self.chl_het_rut= row[48]
        self.chl_het_rutdv= row[49]
        self.cod_causa= row[50]
        self.type_doc_identidad= row[51]
        self.target_giro= row[52]
        self.doc_reverse= row[53]
        self.imp_id= row[54]
        self.source_giro= row[55]
        self.dte_code= row[56]
    def setDetail(self, det):
        self.detail = det

def getGDDet(conn, techkey):
    strsql = "SELECT INV_MOV_TECH_KEY, SEQ_NUM, PRD_LVL_CHILD, PRD_QTY, \
PRD_CST, PRD_PRICE, INV_MOV_TYPE, INV_MOV_NUMBER FROM CHLDDTEE \
WHERE INV_MOV_TECH_KEY = " + techkey.__str__()

    cur = conn.getCursor()
    cur.execute(strsql)
    row = cur.fetchone()
    data = list()
    while(row is not None):
        data.append(Chlddtee(row))
        row = cur.fetchone()
        
    cur.close()
    return data

class Chlddtee:
    def __init__(self, row):
        self.inv_mov_tech_key= row[0]
        self.seq_num= row[1]
        self.prd_lvl_child= row[2]
        self.prd_qty= row[3]
        self.prd_cst= row[4]
        self.prd_price= row[5]
        self.inv_mov_type= row[6]
        self.inv_mov_number= row[7]
    def setTaxes(self, taxes):
        self.taxes = taxes

def getGDTaxes(conn, techkey,seq, prd):
    strsql = "SELECT INV_MOV_TECH_KEY, TXS_CODE_TECH_KEY, SEQ_NUM,PRD_LVL_CHILD, \
TXS_CODE, TXS_RATE, TXS_AMOUNT FROM CHLDDIEE \
WHERE INV_MOV_TECH_KEY = " + techkey.__str__() + " \
AND SEQ_NUM = " + seq.__str__() + " \
AND PRD_LVL_CHILD = " + prd.__str__()

    cur = conn.getCursor()
    cur.execute(strsql)
    row = cur.fetchone()
    data = list()
    while(row is not None):
        data.append(Chlddiee(row))
        row = cur.fetchone()
    cur.close()
    return data

class Chlddiee:
    def __init__(self, row):
        self.inv_mov_tech_key= row[0]
        self.txs_code_tech_key= row[1]
        self.seq_num= row[2]
        self.prd_lvl_child= row[3]
        self.txs_code= row[4]
        self.txs_rate= row[5]
        self.txs_amount= row[6]
