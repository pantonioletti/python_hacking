#coding=UTF-8
'''
Created on Nov 24, 2010

@author: pantonio
'''

fd = open('C:/dev/projects/ScriptsUtil/data/input/falabella_co_equations.txt', 'r')
str = fd.readline()

while len(str)!= 0:
    str = str.replace('\n', '')
    vals = str.rsplit(';')
    d_cd = vals[0][len(vals[0])-3:]
    new_eq = vals[4]
    if d_cd.isdigit():
        idx = vals[4].find('F12')
        if idx > -1 and vals[4][idx+1:idx+4].isdigit():
            new_eq = vals[4].replace(vals[4][idx:idx+4], 'F12_'+ d_cd)
            #print(vals[0] + "=>" + new_eq)
    #print(str)
    print(vals[0].strip()+";"+vals[1].strip()+";"+vals[2].strip()+";"+vals[3].strip()+";"+new_eq.strip()+";"+vals[5].strip()+";"+vals[6].strip())
    str = fd.readline()
    # 0: código ecuación
    # 1: Nombre ecuación
    # 2: Código actividad asociada
    # 3: Tipo (MINUTOS)
    # 4: Ecuación 
    # 5: Org
    # 6: Min Max (Y|N)
