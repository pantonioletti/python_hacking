#coding=ISO_8859-1
'''
Created on 01-10-2009

@author: Pablo Antonioletti
'''
from config.org_api import org_entry_small

class element:
    def __init__(self, id, code, name):
        self.id = id
        self.code = code
        self.name = name
    
class group:
    def __init__(self, id, code, name):
        self.id = id
        self.code = code
        self.name = name

class def_group:
    def __init__(self, group):
        self.group = group
        self.subgroups = dict()
        
    #group: group instance
    def add_subgroup(self, group):
        if group not in self.subgroups:
            self.subgroups[group.code] = group
            
class def_element:
    def __init__(self, element):
        self.element = element
        self.groups = dict()
    
    #group: group code
    def belongs_to(self, group):
        return group in self.groups
    
    # group: def_group instance
    def add_group(self, group):
        if group not in self.groups:
            self.groups[group.code] = def_group(group)
            
    # group: group code; subgroup: group instance
    def add_subgroup(self, group, subgroup):
        if group in self.groups:
            self.groups[group].add_subgroup(subgroup)
        
class definition:
    def __init__(self, code):
        self.code = code
        self.elements = dict()
        
    #element: element instance
    def add_element(self, element):
        if element.code not in self.elements:
            self.elements[element.code] = def_element(element)

    # element: element code            
    def belongs_to(self, element):
        return element in self.elements
    
    # element: element code; group: group instance
    def add_group(self, element, group):
        if element in self.elements:
            if not self.elements[element].belongs_to(group.code):
                self.elements[element].add_group(group)

    # element: element code; group: group code; subgroup: group instance
    def add_subgroup(self, element, group, subgroup):
        if element in self.elements:
            if self.elements[element].belongs_to(group):
                self.elements[element].add_subgroup(group, subgroup)

def print_forecast_body(d_def, d_elem, d_grp):
    str = ''
    d_elem_id_cd = dict()
    for el_cd in d_elem.keys():
        d_elem_id_cd[d_elem[el_cd].id] = el_cd
    d_grp_id_cd = dict()
    for grp_cd in d_grp.keys():
        d_grp_id_cd[d_grp[grp_cd].id] = grp_cd
        
    for def_key in d_def.keys():
        rank_el = 1
        str += '<definition id="' + def_key.__str__() + '" displayName="Definición ' + def_key.__str__() + '" initDaysPrior="7" timeIncrement="' + def_key.__str__() + '" >\n'
        str += '    <defElement elementID="1" initValueType="&INIT_TYPE_TREND;" rank="' + rank_el.__str__() + '" >\n'
        str += '        <projection linkedProjElemID="1" linkedProjTimeFrame="&LINK_TIME_FRAME_DAY;" lockedToProj="N" />\n'
        rank_el += 1
        l_elem_id = list()
        for elem_key in d_def[def_key].elements.keys():
            l_elem_id.append(d_elem[elem_key].id)
        l_elem_id.sort()
        el_iter = iter(l_elem_id)
        for elem_id in el_iter:
            if elem_id != 1:
                str += '        <linkedElement elementID="' + elem_id.__str__() + '" linkPercent="100" />\n'
        str += '        <elementGroup groupID="1" rank="1" />\n'
        str += '    </defElement>\n'

        el_iter = iter(l_elem_id)
        for elem_id in el_iter:
            if elem_id == 1:
                continue 
            str += '    <defElement elementID="' + elem_id.__str__() + ' " initValueType="&INIT_TYPE_PATTERN;" rank="' + rank_el.__str__() + '" >\n'
            rank_el += 1
            rank_grp = 1
            l_grp_id = list()
            for grp_key in d_def[def_key].elements[d_elem_id_cd[elem_id]].groups.keys():
                l_grp_id.append(d_grp[grp_key].id)
            l_grp_id.sort()
            gr_it = iter(l_grp_id)
            for grp_id in gr_it:    
                str += '        <elementGroup groupID="' + grp_id.__str__() + '" rank="' + rank_grp.__str__()
                rank_grp += 1
                d_subgrp = d_def[def_key].elements[d_elem_id_cd[elem_id]].groups[d_grp_id_cd[grp_id]].subgroups
                if len(d_subgrp) > 0:
                    str += '" >\n'
                    rank_subgrp = 1
                    l_sgrp_id = list()
                    for grp_key in d_subgrp.keys():
                        l_sgrp_id.append(d_grp[grp_key].id)
                    l_sgrp_id.sort()
                    sgr_it = iter(l_sgrp_id)
                    for subgrp_id in sgr_it:
                        str += '            <elementGroup groupID="' + subgrp_id.__str__() + '" rank="' + rank_subgrp.__str__() + '" />\n'
                        rank_subgrp += 1
                    str += '        </elementGroup>\n'
                else:
                    str += '" />\n'
            str += '    </defElement>\n'
        str += '    <patterns maxWeeks="13" historyPeriods="24" precision="2" >'
        str += '        <pattern_type id="&PATTERN_TYPE_LAST_X_WEEKS;" default_weeks="3" init_selected="N" />\n'
        str += '        <pattern_type id="&PATTERN_TYPE_SAME_WEEK_LAST_X_YEARS;" default_years="1" init_selected="N" />\n'
        str += '        <pattern_type id="&PATTERN_TYPE_WPY;" default_weeks="1" default_periods="3" default_years="1" init_selected="Y" />\n'
        str += '    </patterns>\n'

        str += '    <trending maxWeeks="13" historyPeriods="24" precision="2" >\n'
        str += '        <pattern_type id="&PATTERN_TYPE_LAST_X_WEEKS;" default_weeks="5" init_selected="Y" />\n'
        str += '        <pattern_type id="&PATTERN_TYPE_SAME_WEEK_LAST_X_YEARS;" default_years="1" init_selected="N" />\n'
        str += '        <pattern_type id="&PATTERN_TYPE_WPY;" default_weeks="2" default_periods="3" default_years="1" init_selected="N" />\n'
        str += '    </trending>\n'
        str += '    <applies-to >\n'
        str += '        <org level="1" applicable="Y" />\n'
        str += '    </applies-to>\n'
        str += '</definition>\n'
    print(str)
    d_el_id_cd = dict()
    l_elem_id = list()
    for elem_key in d_elem.keys():
        d_el_id_cd[d_elem[elem_key].id] = elem_key
        l_elem_id.append(d_elem[elem_key].id)
    l_elem_id.sort()
    el_iter = iter(l_elem_id)
    str = ''
    for el_id in el_iter:
        el_cd = d_el_id_cd[el_id]
        str += '<element id="' + d_elem[el_cd].id.__str__() + '" code="' + d_elem[el_cd].code + '" displayName="' + d_elem[el_cd].name + '" defaultFormat="###,###" />\n'
    print(str)
    
    d_grp_id_cd = dict()
    l_grp_id = list()
    for grp_key in d_grp.keys():
        d_grp_id_cd[d_grp[grp_key].id] = d_grp[grp_key].code
        l_grp_id.append(d_grp[grp_key].id)
    l_grp_id.sort()
    grp_iter = iter(l_grp_id)
    str = ''
    for grp_id in grp_iter:
        grp_cd = d_grp_id_cd[grp_id]
        str += '<group id="' + d_grp[grp_cd].id.__str__() + '" code="' + d_grp[grp_cd].code + '" displayName="' + d_grp[grp_cd].name + '" defaultGroup="N" />\n'

    print(str)

def attr12_org_structure(orgs, groups):
    try:
        fd = open(orgs,'r')
        str = fd.readline()
        d_orgs = dict()

        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            #0:oe.org_entry_name, 
            #1:substr(oe.org_entry_cd,length(oe.org_entry_cd)-3,4), 
            #2:oe.org_level_id, 
            #3:orr.parent_org_id, 
            #4:orr.child_org_id            
            if (vals[4] in groups):
                new_org = org_entry_small()
                new_org.id = vals[4]
                new_org.code = vals[1]
                if (vals[2] == '5'):
                    if (vals[3] in d_orgs):
                        parent = d_orgs[vals[3]]
                        parent.positions[new_org.id] = new_org
                    else:
                        print('Parent not found')
                else:
                    d_orgs[new_org.id] = new_org

            str = fd.readline()
        fd.close()
    except IOError:
        print ("File ", orgs, " not found")


def load_forecast(fore):
    d_def = dict()
    d_elem = dict()
    d_grp = dict()
    l_g_code = list()
    l_e_code = list()
    
    first_g= 'Default'
    first_e = 'Ventas'
    
    try:
        fd = open(fore, 'r')
        str = fd.readline()
        while(len(str) != 0):
            str = str.replace('\n', '')
            str = str.replace('DEFAULT', 'Default')
            vals = str.rsplit(';')
            #0: Definition 15MIN;
            #1: Element Display name Atención de Vta en Piso;
            #2: Element NATE;
            #3: Group display name At.Vta Piso-Acc. Muj.;
            #4: Group D101
            #5: Sub-Group display name At.Vta Piso-Acc. Muj.;
            #6: Sub-Group D101
            #===================================================================
            # Definition;
            # Element;
            # Element Display Name;
            # Group Code;
            # Group Display Name;
            # Group Code;
            # Group Display Name;
            # Forecast Parameter Name;
            # Interface Forecast Code;
            # Forecast Code
            #===================================================================
            if (len(vals) > 5):
                if (not vals[0] in d_def):
                    o_def = definition(vals[0])
                    d_def[vals[0]] = o_def
                if len(vals[1]) > 0:
                    # Add element to elements dict
                    if vals[2] not in d_elem:
                        d_elem[vals[1]] = element(0, vals[1], vals[2])
                        if vals[1] != first_e:
                            l_e_code.append(vals[1])
                    #Add a reference to element in definition
                    if not d_def[vals[0]].belongs_to(vals[1]):
                        d_def[vals[0]].add_element(d_elem[vals[1]])
                    if len(vals[3]) > 0:
                        #Add group to groups dict
                        if vals[3] not in d_grp:
                            d_grp[vals[3]] = group(0, vals[3], vals[4])
                            if vals[3] != first_g:
                                l_g_code.append("0" + vals[3])
                        d_def[vals[0]].add_group(vals[1], d_grp[vals[3]])
                        if len(vals[5]) > 0:
                            if vals[5] not in d_grp:
                                d_grp[vals[5]] = group(0, vals[5], vals[6])
                                if vals[5] != first_g:
                                    l_g_code.append("1" + vals[5])
                            d_def[vals[0]].add_subgroup(vals[1], vals[3], d_grp[vals[5]])
                
            str = fd.readline()
        fd.close()
        l_e_code.sort()
        l_g_code.sort()
        d_elem[first_e].id = 1
        d_grp[first_g].id = 1
        elem_id = 2
        group_id = 100
        for i in range(len(l_e_code)):
            d_elem[l_e_code[i]].id=elem_id
            elem_id += 1
        for i in range(len(l_g_code)):
            if i > 0:
                if l_g_code[i][0] != l_g_code[i-1][0]:
                    group_id += 100
            d_grp[l_g_code[i][1:]].id=group_id
            group_id += 1

    except IOError:
        print ("File ", fore, " not found")
    return ([d_def, d_elem, d_grp])    

    