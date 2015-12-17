__author__ = 'pantonio'

import psycopg2
import GPA_Config
from sys import argv
from time import time


def get_bus(filter):

    stmt = "select distinct business_unit from wfmr_bu_user "

    conn = psycopg2.connect(host=GPA_Config.pgsql_conn_str["host"], \
                            port=GPA_Config.pgsql_conn_str["port"], \
                            database=GPA_Config.pgsql_conn_str["database"], \
                            user=GPA_Config.pgsql_conn_str["user"], \
                            password=GPA_Config.pgsql_conn_str["password"])
    cur = conn.cursor()
    if filter is not None:
        stmt = stmt + filter
    cur.execute(stmt)
    stores = cur.fetchall()
    conn.close()
    return stores

def get_users_by_bu(bu):
    stmt = "select wu.login_name,wu.status,wu.first_name,wu.last_name,wu.default_language_name, " \
           "wu.role_id,bu.business_unit,we.birth_date,we.hire_date,we.gender,we.punch_validation, "\
           "we.employee_type,we.login_name,we.scheduling_type_code,we.work_unassigned_flag, "\
           "we.manager_in_scheduling_flag, we.employee_generates_exception, we.employee_generates_alerts, " \
           "ej.job_id, ej.start_date, ej.pay_policy_id, ej.punch_rule_id,ej.shift_strategy_id, ej.rate " \
           "from wfmr_user wu, wfmr_bu_user bu, wfmr_emp we, wfmr_emp_job ej "\
           "where bu.login_name = wu.login_name "\
           "and we.login_name = wu.login_name "\
           "and ej.login_name = wu.login_name "\
           "and bu.business_unit = '" + bu + "'" # and wu.login_name = '565408'"

    conn = psycopg2.connect(host=GPA_Config.pgsql_conn_str["host"], \
                            port=GPA_Config.pgsql_conn_str["port"], \
                            database=GPA_Config.pgsql_conn_str["database"], \
                            user=GPA_Config.pgsql_conn_str["user"], \
                            password=GPA_Config.pgsql_conn_str["password"])
    cur = conn.cursor()
    cur.execute(stmt)
    users = cur.fetchall()
    conn.close()
    return users

def emp_to_deact(file_path, prefix):
    fd = open(file_path,'r')
    line = fd.readline()
    d_users= dict()
    while len(line) > 0:
        line = line.replace('\n','')
        data = line.split(';')
        if len(data)>1:
            if data[2] not in d_users:
                d_users[data[2]] = list()
            d_users[data[2]].append(prefix+data[1])
        line = fd.readline()
    fd.close()
    return d_users

def deactivate_emps(path, l_emp):
    fd = open('{0}\\emp_to_deact_{1:.0f}.xml'.format(path,time()), mode='w', encoding='utf-8')
    fd.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
    fd.write("<EnterpriseDocument InterfaceName=\"Employee Interface\" Version=\"2.0\" CreationSource=\"GPA\" CreationTimestamp=\"2015-05-20T00:00:00\">\n")
    fd.write("<BusinessUnitList>\n")
    for bu in l_emp.keys():
        fd.write("<BusinessUnit id=\"" + bu +"\">")
        for usr in l_emp[bu]:
            fd.write( '<User id="{0}" loginName="{1}" statusCode="i" >\n'.format(usr, usr))
            fd.write('<Employee badgeNumber="{0}" >\n'.format(usr))
            fd.write('<WorkStatusList>\n<WorkStatus start="2015-10-01" action="h" status="i" />\n</WorkStatusList>\n')
            fd.write('</Employee>')
            fd.write('</User>\n')
        fd.write("</BusinessUnit>\n")
    fd.write("</BusinessUnitList>\n")
    fd.write("</EnterpriseDocument>\n")
    fd.close()

if len(argv) < 2:
    print("Exiting!!!!")
    exit()

cmd = argv[1]
path = argv[2]
if cmd == 'deact':
    sflist = argv[3]
    l_emp = emp_to_deact(sflist,'')
    deactivate_emps(path, l_emp)

elif cmd == 'export':
    path = argv[2]
    filter = " where business_unit in ('0608') "
    '''
    '0271','1686','1687','1688'
    " where business_unit in ('0007','0016','0020','0021','0025','0056','0076','0087','0088','0107','0147',"\
            "'0149','0168','0271','0516','0531','0597','0608','0646','1013','1302','1307',"\
            "'1308','1309','1310','1314','1315','1317','1319','1320','1321','1322','1326',"\
            "'1337','1338','1341','1350','1352','1356','1357','1359','1360','1364','1377',"\
            "'1384','1388','1390','1391','1397','1612','1669','1686','1687','1688','1703',"\
            "'1706','1707','1708','1710','1711','1712','1713','1715','1718','1723','1726',"\
            "'1729','1734','1738','1759','1760','1761','1762','1763','1765','1766','1769',"\
            "'1771','1785','1786','1788','1789','1790','1792','1793','1794','1796','1802',"\
            "'1806','1807','1808','1810','1811','1812','1814','1819','1848','1849','1850',"\
            "'1852','1854','1857','1858','1859','1860','1863','1864','1867','1877','1879',"\
            "'1887','1893','2056','2065','2066','2075','2135','2326','2404','2410','2412',"\
            "'2426','2427','2428','2429','2430') "
    '''
    bus = get_bus(filter) # where business_unit = '1388'")

    print('# of BUs to proc: {0}\n'.format(len(bus)))
    for bu in bus:

        fd = open(path+'\\emp_bu_'+bu[0]+'.xml', mode='w', encoding='utf-8')
        fd.write("<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n")
        fd.write("<EnterpriseDocument InterfaceName=\"Employee Interface\" Version=\"2.0\" CreationSource=\"GPA\" CreationTimestamp=\"2015-05-20T00:00:00\">\n")
        fd.write("<BusinessUnitList>\n")

        fd.write("<BusinessUnit id=\"" + bu[0] +"\">")
        users = get_users_by_bu(bu[0])
        for user in users:
            line = '<User id="'+ user[0] + '" '
            line += 'loginName="'+ user[0] + '" '
            line += 'statusCode="'+user[1]+'" '
            line += 'firstName="'+user[2]+'" '
            line += 'lastName="'+user[3]+'" '
            line += 'forcePasswordChange="y" password="0000" '
            line += 'defaultLanguageName="'+user[4]+'">\n'
            #line += '<RoleList><Role id="'+user[5]+'"/></RoleList>\n'
            line += '<RoleList><Role id="GPA Worker"/></RoleList>\n'
            line += '<OrgList><Organization id="'+ bu[0] +'"/></OrgList>\n'
            line += '<Address country="BR" ></Address>\n'
            line += '<Employee birthDate="'+user[7].year.__str__()+'-'
            if user[7].month < 10:
                line+= '0'
            line += user[7].month.__str__()+'-'
            if user[7].day < 10:
                line+= '0'
            line+= user[7].day.__str__()+ '" '
            line += 'hireDate="'+user[8].year.__str__()+'-'
            if user[8].month < 10:
                line+= '0'
            line += user[8].month.__str__()+'-'
            if user[8].day < 10:
                line+= '0'
            line+= user[8].day.__str__()+ '" '
            line += 'gender="'+user[9]+'" '
            line += 'punchValidation="'+user[10]+'" '
            line += 'employeeType="'+user[11]+'" '
            line += 'badgeNumber="'+user[12]+'" '
            line += 'schedulingTypeCode="'+user[13]+'" '
            line += 'workUnassignedFlag="'+user[14]+'" '
            line += 'employeeGeneratesExceptions="'+user[15]+'" '
            line += 'managerLevelFlag="n" managerInSchedulingFlag="n" '
            line += 'employeeGeneratesAlerts="'+user[16]+'">\n'
            line += '<JobList>\n'
            line += '<Job id="'+user[18]+'" '
            line += 'start="'+user[19].__str__()+'" >\n'
            line += '<PrimaryJobInfo payPolicyId="'+user[20]+'" '
            line += 'punchRuleId="'+user[21]+'" '
            line += 'shiftStrategyId="'+user[22]+'"/>\n'
            line += '<JobRate start="'+user[19].year.__str__()+'-'
            if user[19].month < 10:
                line+= '0'
            line += user[19].month.__str__()+'-'
            if user[19].day < 10:
                line+= '0'
            line += user[19].day.__str__()+'" '
            line += 'rate="'+user[23].__str__()
            line += '"/>\n'
            line += '</Job>\n'
            line += '</JobList>\n'
            line += '<WorkStatusList>\n'
            line += '<WorkStatus start="'+user[19].year.__str__()+'-'
            if user[19].month < 10:
                line+= '0'
            line += user[19].month.__str__()+'-'
            if user[19].day < 10:
                line+= '0'
            line += user[19].day.__str__()+'" '
            line += 'action="h" status="a" />\n'
            line += '</WorkStatusList>\n'
            line += '</Employee>\n'
            line += '</User>'
            fd.write(line)


        fd.write("</BusinessUnit>\n")
        fd.write("</BusinessUnitList>\n")
        fd.write("</EnterpriseDocument>\n")
        fd.close()
        fd = open(path+'\\emp_bu_'+bu[0]+'.xml.flag', mode='w')
        fd.close()
