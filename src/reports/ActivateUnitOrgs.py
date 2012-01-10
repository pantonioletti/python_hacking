import os
import sys
import cx_Oracle
import xml.dom
from reports.PWMRepCommon import buildConnStr
from reports.PWMRepCommon import getAllChildren
from xml.dom import getDOMImplementation

def ActivateOrg(connStr, org_cd, status, eff_date, output_file, parent_rel=False):
    assert (status is not None), print('Org status is None\n')
    assert (eff_date is not None), print('Org status eff date is None\n')
    orgs = getAllChildren(connStr, org_cd)
    if (orgs is None):
        return
    dom_imp = getDOMImplementation()
    org_api_int = dom_imp.createDocument('orgapiload', 'orgapiload', None)
    root_element = org_api_int.documentElement
    root_element.setAttribute("global_version", "1.0")
    for i in range(0, len(orgs)):
        assert (orgs[i].code is not None), print ('Org entry code is None \n')
        assert (orgs[i].level is not None), print('Org entry level code is None for org ' + orgs[i].code + '\n')
        #assert (orgs[i].location is not None), print('Org location name is None for org ' + orgs[i].code + '\n')
        assert (orgs[i].name is not None), print('Org entry name is None for org ' + orgs[i].code + '\n')

        if orgs[i].location is None:
            orgs[i].location = orgs[i].name 

        org_entry_node = org_api_int.createElement("entry")
        root_element.appendChild(org_entry_node)
        org_entry_node.setAttribute("org_cd", orgs[i].code)
        org_entry_node.setAttribute("org_level_cd", orgs[i].level)
        org_entry_node.setAttribute("locationname", orgs[i].location)
        org_entry_node.setAttribute("name", orgs[i].name)
        status_node = org_api_int.createElement("status")
        status_node.setAttribute("code", status)
        status_node.setAttribute("eff_date", eff_date)
        org_entry_node.appendChild(status_node)
        if (parent_rel and orgs[i].parent_cd is not None):
            assert (orgs[i].parent_level is not None), print ('Parent level code is None for org ' + orgs[i].code + '\n')
            assert (orgs[i].parent_eff_date is not None), print('Parent eff date is None for org ' + orgs[i].code + '\n')
            orgrel_node = org_api_int.createElement("orgrel")
            orgrel_node.setAttribute("org_cd", orgs[i].parent_cd)
            orgrel_node.setAttribute("org_org_lvl_cd", orgs[i].parent_level)
            orgrel_node.setAttribute("eff_date", orgs[i].parent_eff_date.__str__())
            org_entry_node.appendChild(orgrel_node)

    fd = open(output_file, 'w')
    fd.write(org_api_int.toxml())#"iso-8859-1"))
      #print org_api_int.toxml() >> fd
      #"iso-8859-1")
    fd.close()
          #print hijos_rows[j][0], hijos_rows[j][1], hijos_rows[j][2], hijos_rows[j][3]
    

