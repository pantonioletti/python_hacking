'''
Created on 29/08/2011

@author: pantonio
'''
from zipfile import ZipFile
from zipfile import is_zipfile
from xml.dom.minidom import parse

def open(file):
    myzip = None
    if is_zipfile(file):
        myzip = ZipFile(file,'r')
    return myzip

def getExcelData(file):
    myzip = open(file)
    #info_list = myzip.infolist()
    #for file_info in info_list:
    #    print(file_info.filename) 
    wb_doc = parse(myzip.open('xl/workbook.xml', 'r'))
    root = wb_doc.documentElement
    elem_list = root.getElementsByTagName('sheets')
    elem = elem_list[0]
    elem_list = elem.getElementsByTagName('sheet')
    for next_el in elem_list:
        print('Name: ' + next_el.getAttribute('name') + ' || Id: ' + next_el.getAttribute('r:id'))
    
    #sheets = root.getElementsByTagName('sheets').getElementsByTagName('sheet')
    myzip.close()

    
    #ss_xml = myzip.open('xl\sharedStrings.xml', 'r')
        