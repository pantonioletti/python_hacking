##from reports.ActivateUnitOrgs import ActivateOrg
import time
import sys
from reports import PWMRepCommon
from reports.PWMRepCommon import buildConnStr #buildJDBCConnStr
from reports.EmployeesWORotation import empWithoutRot
from reports.EmployeesWORotation import multiRotEmployees
from reports.DupSalesLM import dupSalesLM
from reports.EmployeesWORotation import compOrgPosition
from reports.ActivateUnitOrgs import ActivateOrg
#from .UnbalancedRotations import UnbalancedRotations

##def launchActivateOrg(connStr, output):
##    org_code = "1737"
##    ActivateOrg(connStr, org_code, output)
def launchSalesLMCleanning(connStr, output):
    for org in (("438", "439", "1201", "1737", "2640", "2214", "2775", "3296","9001","530","1445","2381")):
        to_del = dupSalesLM(connStr, output, org, "20080526", "20080622")
        #print to_del
    
def launchMultiRotEmp(connstr, output):
    for org in (("438", "439", "1201", "1737", "2640", "2214", "2775", "3296","9001","530","1445","2381")):
        multiRotEmployees(connstr, "20080623", "20080630", org, output)
    
def launchEmpWORot(connStr, output, params):
    orgs = params[2]
    ##[("1201"),("1737"),("2214"),("2775"),("438"), ("439"), ("2640"), ("3296")]
    for i in range(0, len(orgs)):
        empWithoutRot(connStr,params[0], params[1], orgs[i], output)

def launchRotbalance(connStr, output):
    org_cd = "1737-302"
    sdate = "20080530"
    edate = "20080531"
    #UnbalancedRotations(org_cd, connStr, sdate, edate, output)
    
def launchValOrg(connStr, output):
    start_sdate = '20080805'
    end_sdate = ''
    org_cd = 'JDA'
    org_mod = 'JDA'
    compOrgPosition(connStr, start_sdate, end_sdate, org_cd, org_mod, output)
    
def launchActOrg(connStr, output, params):
    
    #org_cd = "9001"
    #status = "Inactive"
    #eff_date = "1/1/2008"
    ActivateOrg(connStr, params[0], params[1], params[2], output, True)

def launch(report, output, service, user, passwd, params):
    
    connStr = buildConnStr(user, passwd, service)
    rear = time.time().__str__() + ".txt"
    if (report == "SINROT"):
        launchEmpWORot(connStr, output + "ewrot" + rear, params)
    elif (report == "ROTBAL"):
        launchRotbalance(connStr, output + "brot" + rear)
    elif (report == "MULTIROT"):
        launchMultiRotEmp(connStr, output+ "mrot" + rear)
    elif (report == "DELSALES"):
        launchSalesLMCleanning(connStr, output+ "dels" + rear)
    elif (report == "COMPORG"):
        launchValOrg(connStr, output+ "comp" + rear)
    elif (report == "ACTORG"):
        rear = time.time().__str__() + ".xml"
        launchActOrg(connStr, output+ "actorgapi" + rear, params)
    
