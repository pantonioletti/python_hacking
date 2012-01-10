'''
Created on 30/08/2011

@author: pantonio
'''

from util.ziputil import open as zopen
from xml.dom.minidom import parse
from xml.sax import ContentHandler
from xml.sax import make_parser

MODEL_FILE = 'EnterpriseModel'
ORG_LEVELS = 'OrgLevels'
ORG_ENTRIES = 'OrgEntries'
ORG_GROUPS = 'OrgGroups'
STORE_TIME = 'StoreTime'
FISCAL_CAL = 'FiscalCalendar'
ORG_ATTR = 'OrgAttr'

class SharedStringsHandler(ContentHandler):
    
    new_string = False
    my_str=""
    
    def __init__(self, str_list):
        self.str_list = str_list
    def startElement(self,name, attrs):
        #print(name)
        if name == 't':
            self.new_string = True
    def endElement(self,name):
        if name == 't':
            self.new_string = False
            self.str_list.append(self.my_str)
            self.my_str=""
    def characters(self,chars):
        if self.new_string:
            self.my_str += chars
            
class worksheet:
    def __init__(self, name):
        self.name = name
        self.doc = None
        
def load_entreprise_model(file):
    #load worksheet mapping
    fd = open(file, 'r')
    str = fd.readline()
    model=''
    sheets=dict()
    name_sheet= dict()
    while(len(str)!=0):
        str = str.replace('\n', '')
        vals=str.split('=')
        if vals[0] == MODEL_FILE:
            model = vals[1]
        elif vals[0] == ORG_LEVELS:
            sheets[ORG_LEVELS]=worksheet(vals[1])
            name_sheet[vals[1]]=sheets[ORG_LEVELS]
        elif vals[0] == ORG_ENTRIES:
            sheets[ORG_ENTRIES]=worksheet(vals[1])
            name_sheet[vals[1]]=sheets[ORG_ENTRIES]
        elif vals[0] == ORG_GROUPS:
            sheets[ORG_GROUPS]=worksheet(vals[1])
            name_sheet[vals[1]]=sheets[ORG_GROUPS]
        elif vals[0] == STORE_TIME:
            sheets[STORE_TIME]=worksheet(vals[1])
            name_sheet[vals[1]]=sheets[STORE_TIME]
        elif vals[0] == FISCAL_CAL:
            sheets[FISCAL_CAL]=worksheet(vals[1])
            name_sheet[vals[1]]=sheets[FISCAL_CAL]
        elif vals[0] == ORG_ATTR:
            sheets[ORG_ATTR]=worksheet(vals[1])
            name_sheet[vals[1]]=sheets[ORG_ATTR]
        str = fd.readline()
    fd.close()
    err_msg = ''
    if len(model) == 0:
        err_msg = 'Missing reference to Enterprise model file\n'
    if ORG_LEVELS not in sheets:
        err_msg += 'Missing reference to organization level worksheet\n'
    if ORG_ENTRIES not in sheets:
        err_msg += 'Missing reference to organization entries worksheet\n'
    if ORG_GROUPS not in sheets:
        err_msg += 'Missing reference to organization groups worksheet\n'
    if STORE_TIME not in sheets:
        err_msg += 'Missing reference to store open/close time worksheet\n'
    if FISCAL_CAL not in sheets:
        err_msg += 'Missing reference to fiscal calendar worksheet\n'
    if ORG_ATTR not in sheets:
        err_msg += 'Missing reference to organization attributes worksheet\n'

    ret_val = None
    if len(err_msg) > 0:
        print(err_msg)
    else:
        getExcelData(model, sheets, name_sheet)
        
    return ret_val


def getRelationships(file):
    doc = parse(file)
    root = doc.documentElement
    elem_list = root.getElementsByTagName('Relationship')
    rels = dict()
    for next_el in elem_list:
        rels[next_el.getAttribute('Id')] = next_el.getAttribute('Target')
    return rels

def getStringList(str_doc):
    str_list = list()
    parser = make_parser()
    parser.setContentHandler(SharedStringsHandler(str_list))
    parser.parse(str_doc)
    return str_list

def getExcelData(model, sheets, name_sheet):
    myzip = zopen(model)
    
    rels = getRelationships(myzip.open('xl/_rels/workbook.xml.rels'))
    strs= getStringList(myzip.open('xl/sharedStrings.xml'))
    wb_doc = parse(myzip.open('xl/workbook.xml', 'r'))
    root = wb_doc.documentElement
    elem_list = root.getElementsByTagName('sheets')
    elem = elem_list[0]
    elem_list = elem.getElementsByTagName('sheet')
    for next_el in elem_list:
        name = next_el.getAttribute('name')
        id = next_el.getAttribute('r:id')
        if name in name_sheet and id in rels:
            name_sheet[name].doc=parse(myzip.open('xl/'+rels[id], 'r'))
        #print('Name: ' + name + ' || Id: ' + id + ' || File: ' + rels[id])
    
    #sheets = root.getElementsByTagName('sheets').getElementsByTagName('sheet')
    myzip.close()