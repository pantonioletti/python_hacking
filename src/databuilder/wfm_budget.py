'''
Created on Jan 4, 2010

@author: pantonio
'''
from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import random
import time
import math

class BudgetHandler(ContentHandler):
    def __init__(self):
        self.data = dict()
        
    def startElement(self, name, attrs):
        if (name == 'budgetdata'):
            org_cd = attrs.get('org_cd', "")
            #org_lvl = attrs.get('org_level_cd', "")
            date = attrs.get('date', "00000000")
            val = float(attrs.get('value', "0.0"))
            day = int(date[6:8])
            if (org_cd not in self.data):
                self.data[org_cd]=dict()
                self.data[org_cd][31]=val
            self.data[org_cd][day] = val
            
        
def build_budget(data):
    parser = make_parser()
    handler = BudgetHandler()
    parser.setContentHandler(handler)
    parser.parse(open(data))
    
    data = parser.getContentHandler().data
    if (data is not None):
        random.seed(time.time())
        print('<?xml version="1.0" encoding="ISO-8859-1"?>\n')
        print('<!DOCTYPE budgetload>\n')
        print('<budgetload global_version="1.0">')
        tm = ['200804', '200805','200806', '200807','200808', '200809','200810', '200811','200812', '200901','200902', '200903','200904', '200905','200906', '200907','200908', '200909','200910', '200910','200911', '200912']
        for month in tm: #range(1,13):
            for dp in data.iterkeys():
                for day in iter(data[dp]):
                    if (month[4:6] == '02' and day > 28):
                        continue
                    if (month[4:6] in ['04','06','09','11'] and day > 30):
                        continue
                    str = '<budgetdata org_cd = "'
                    str += dp + '" org_level_cd = "DP" year = "0" period = "0" sub_period = "0" sub_sub_period = "0" date = "'
                    sd = ''
                    if (day < 10):
                        sd = '0' 
                    sd += day.__str__()
                    str += month + sd + '" element_cd = "ASalesD" account = "1" value = "'
                    str +=  round(data[dp][day],1).__str__() + '" > </budgetdata>'
                    print(str)
                    inc = 1 + (random.random()/50)
                    data[dp][day] = data[dp][day]*inc 
        print('</budgetload>\n')
    #<budgetdata org_cd = "PEDP0040D101" org_level_cd = "DP" year = "0" period = "0" sub_period = "0" sub_sub_period = "0" date = "20090401" element_cd = "ASalesD" account = "1" value = "782.8" > </budgetdata>


build_budget('c:/temp/ripley/WFM_BUDGET20091230.xml.091230112753')