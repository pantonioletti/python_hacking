#coding=ISO_8859-1
'''
Created on Nov 24, 2009

@author: pantonio
'''
def filter(file, white_list):
    try:
        fd = open(file, 'r')
        str = fd.readline()
        while(len(str) != 0):
            str = str.replace('\n', '')
            for f in white_list:
                if f in str:
                    print(str)
                    str = fd.readline()
                    str = str.replace('\n', '')
                    print(str)
                    break
            str = fd.readline()
        fd.close()
    except IOError:
        print ("File ", file, " not found")
    return None

x=filter("c:/dev/projects/pwmpython/dbabs2.log",["insert","delete","update",])