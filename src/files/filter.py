#coding=ISO_8859-1
'''
Created on Nov 24, 2009

@author: pantonio
'''
def filter(file, white_list, black_list):
    try:
        fd = open(file, 'r')
        str = fd.readline()
        while(len(str) != 0):
            str = str.replace('\n', '')
            ok = False
            to_print = ""
            for f in white_list:
                if 'SQL:' in str and f in str.lower():
                    to_print = str
                    if ('?' in str):
                        str = fd.readline()
                        str = str.replace('\n', '')
                        to_print += '\n'
                        to_print += str
                    ok = True
                    break
            if ok:
                for f in black_list:
                    if f in to_print.upper():
                        ok = False
                        break
            if ok:
                print(to_print)
            str = fd.readline()
        fd.close()
    except IOError:
        print ("File ", file, " not found")
    return None

x=filter("c:/dev/projects/pwmpython/dbabs2.log",["insert","delete","update",],["EVENT_SYNC", "DEVEL_TASK_AUDIT","EWM_TABLE_LOCK","SYSTEM_STATS",])