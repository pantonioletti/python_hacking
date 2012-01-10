'''
Created on Apr 19, 2010

@author: pantonio
'''
def act_wo_position(act_u, act_wo_p):
    fd1 = open(act_u, 'r')
    
    act_u_set = set()
    
    act_cd = fd1.readline()
    while len(act_cd) != 0:
        act_cd = act_cd.replace('\n', '')
        act_u_set.add(act_cd)
        act_cd = fd1.readline()
    fd1.close()
    
    fd2 = open(act_wo_p)
    #act_wo_p_d = dict()
    
    str = fd2.readline()
    while len(str) != 0:
        str = str.replace('\n', '')
        vals = str.split(';')
        if vals[1] not in act_u_set:
            print(str)
        str = fd2.readline()
    fd2.close()