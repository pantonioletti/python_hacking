#coding=ISO_8859-1
'''
Created on Apr 6, 2010

@author: pantonio
'''

class org:
    def __init__(self, cd, name, level, parent):
        self.cd = cd
        self.name = name
        self.level = level
        self.parent = parent
        self.children = dict()
    def add_child(self, child):
        self.children[child.cd] = child
        
def load_orgs(file):
        fd = open(file,'r')
        str = fd.readline()
        d_orgs = dict()

        while(len(str) != 0):
            str = str.replace('\n', '')
            vals = str.rsplit(';')
            o_org = org(vals[0][8:], vals[1], vals[2], vals[3][8:])
            #print(o_org.cd + "#" + o_org.parent)
            d_orgs[o_org.cd] = o_org
            if o_org.level == 'WG':
                d_orgs[o_org.parent].add_child(o_org)
            str = fd.readline()
        fd.close()
        group_id = 1
        for key in d_orgs.keys():
            if d_orgs[key].level == 'UE':
                #print('<group displayName="' + d_orgs[key].name + '" groupID="' + group_id.__str__() + '" typeAttrVal = "' + d_orgs[key].cd + '" >')
                print('<group displayName="' + d_orgs[key].name + '" groupID="' + group_id.__str__() + '" >')
                group_id += 1
                for wg_key in d_orgs[key].children.keys():
                    print('    <level displayName="' + d_orgs[key].children[wg_key].name + '" typeAttrVal = "' + d_orgs[key].children[wg_key].cd + '" />')
                print('</group>')
 