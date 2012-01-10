'''
Created on Nov 23, 2010

@author: pantonio
'''
import sys

def get_activities(conn):

    act_cd_id = dict()
    try:
        cursor = conn.cursor()    
        sql = "SELECT ACTIVITY_ENTRY_CD, ACTIVITY_ENTRY_ID FROM ACTIVITY_ENTRY"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for one_row in rows:
            act_cd_id[one_row[0]] = one_row[1]
        cursor.close()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    return act_cd_id

def get_forecast_groups(conn):

    og_cd_id = dict()
    try:
        cursor = conn.cursor()    
        sql = "SELECT FORECAST_GROUP_CD, FORECAST_GROUP_ID FROM FORECAST_GROUP"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for one_row in rows:
            og_cd_id[one_row[0]] = one_row[1]
        cursor.close()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    return og_cd_id

def get_forecast_element(conn):

    og_cd_id = dict()
    try:
        cursor = conn.cursor()    
        sql = "SELECT FORECAST_ELEMENT_CD, FORECAST_ELEMENT_ID FROM FORECAST_ELEMENT"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for one_row in rows:
            og_cd_id[one_row[0]] = one_row[1]
        cursor.close()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    return og_cd_id

def get_forecast_def(conn):

    og_cd_id = dict()
    try:
        cursor = conn.cursor()    
        sql = "SELECT FORECAST_DEF_CD, FORECAST_DEF_ID FROM FORECAST_DEFINITION"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for one_row in rows:
            og_cd_id[one_row[0]] = one_row[1]
        cursor.close()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    return og_cd_id

def get_org_entries(conn):

    og_cd_id = dict()
    try:
        cursor = conn.cursor()    
        sql = "SELECT ORG_ENTRY_CD, ORG_ENTRY_ID FROM ORG_ENTRY"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for one_row in rows:
            og_cd_id[one_row[0]] = one_row[1]
        cursor.close()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    return og_cd_id

def get_org_groups(conn):

    og_cd_id = dict()
    try:
        cursor = conn.cursor()    
        sql = "SELECT ORG_GROUP_CD, ORG_GROUP_ID FROM ORG_GROUP"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for one_row in rows:
            og_cd_id[one_row[0]] = one_row[1]
        cursor.close()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    return og_cd_id

def get_uom(conn):

    uom_cd_id = dict()
    try:
        cursor = conn.cursor()    
        sql = "SELECT UOM_CD, UOM_ID FROM UOM"
        cursor.execute(sql)
        rows = cursor.fetchall()
        for one_row in rows:
            uom_cd_id[one_row[0]] = one_row[1]
        cursor.close()
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    return uom_cd_id
