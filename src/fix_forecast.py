'''
Created on Nov 30, 2010

@author: pantonio
'''
from file.read_filesystem import read_filesystem
from sys import argv
import os


def rename_files(path):
    files = read_filesystem(path)
    for f in files:
        new_name = f.replace('.txt', '')
        os.rename(f, new_name)

def fix_forecast2(path):
    files = read_filesystem(path)
    for f in files:
        fd1 = open(f,'r')
        fd2 = open(f+'.txt', 'w')
        str = fd1.readline()
        while (len(str) > 0):
            new_str = str
            start_idx = str.find('account="')
            if start_idx > -1:
                end_idx = str.find('"', start_idx+9)
                if end_idx > start_idx:
                    group_cd = str[start_idx+9:end_idx]
                    if group_cd.find(',') > -1:
                        codes = group_cd.split(',')
                        new_group_cd = codes[1]+','+codes[0]
                        new_str = str.replace('account="'+group_cd,'account="'+new_group_cd)
            fd2.write(new_str)
            str = fd1.readline()
        fd1.close()
        fd2.close()
    #account="CAMB,302"    
def fix_forecast(path):
    files = read_filesystem(path)
    
    for f in files:
        fd1 = open(f,'r')
        fd2 = open(f+'.txt', 'w')
        str = fd1.readline()
        while (len(str) > 0):
            new_str = str.replace('org_level_cd="LOCAL"', 'org_level_cd="LOC"')
            fd2.write(new_str)
            str = fd1.readline()
        fd1.close()
        fd2.close()
        
fix_forecast2(argv[1])
