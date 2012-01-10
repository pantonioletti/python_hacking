'''
Created on 08-09-2009

@author: pantonio
'''
import os
import subprocess

def decompile_java(decomp, path):
    files = read_filesystem(path)
    for idx in range(0,len(files)):
        if files[idx].__str__().endswith('.class'):
            output = files[idx].__str__().replace('.class','.java')
            l = list()
            l = l + decomp
            l.append(files[idx])
            l.append('>')
            l.append(output)
            execute(l)
            #print(files[idx].__str__() + '\n')
    
def read_filesystem(path):
    if not os.path.exists(path):
        return None
    files = list()
    if os.path.isdir(path):
        subdirs = os.listdir(path)
        for f in subdirs:
            next_f = path + '/' + f
            sd_files = read_filesystem(next_f)
            if (sd_files is not None):
                files = files + sd_files
    else:
        files.append(path)
    return files

def execute(to_exec):
    pid = -1
    try:
        pid = subprocess.call(to_exec)
    except OSError:
        print('F... off I didn''t found the bloody file')
    return pid
    
