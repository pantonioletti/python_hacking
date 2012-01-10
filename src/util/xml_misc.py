#coding=UTF-8
#XXXXXwindows-1252
#XXXISO_8859-1
'''
Created on Jan 7, 2010

@author: pantonio
'''
def rename_massive(file):
    fd = open(file, 'r')
    str = fd.readline()
    while(len(str) != 0):
        str = str.replace('\n', '')
        old_name = str
        vals = str.rsplit('.xml.')
        print("move " + old_name + " " + vals[0] + ".xml")
        str = fd.readline()
    fd.close()

def add_new_line(file, path_from, path_to, to_find):
    try:
        fd = open(path_from + file, 'r')
        fd2 = open(path_to + file , 'w+')
        buffer_len=1024
        chr = fd.read(buffer_len)
        
        while(len(chr) != 0):
            str = ''
            rear=''
            pos=0
            idx=chr.find(to_find)
            if idx > -1:
                pos=idx+len(to_find)
                rear = '\n'
            else:
                if len(chr) > len(to_find):
                    pos=len(chr)-len(to_find)+1
            str=chr[:pos]+rear
            chr=chr[pos:]
            #if chr.find('<t>DIVISI') > -1:
            #    pass
            if len(chr) <= len(to_find):
                try:
                    chr += fd.read(buffer_len)
                except UnicodeDecodeError:
                    print(chr)
                    raise
                if len(chr) < len(to_find):
                    str += chr
                    chr=''
            fd2.write(str)
        fd2.close()
        fd.close()
    except IOError:
        raise
    
def print_emp_to_process(file, path_to, to_find):
    try:
        head = '<?xml version="1.0" encoding="UTF-8"?><empload global_version="1.0">\n'
        tail = '</empload>'
        fd = open(file, 'r')
        line = fd.readline()
        counter = 1
        while len(line)!= 0:
            line = line.replace('\n', '')
            for emp_id in to_find:
                if line.find('emp_cd="'+emp_id+'"') != -1:
                    try:
                        fd2 = open(path_to + emp_id + '.xml' , 'w+')
                        fd2.write(head)
                        fd2.write(line)
                        fd2.write('\n')
                        fd2.write(tail)
                        fd2.close()
                    except Exception:
                        print(str(Exception))
                        print("at line : " + counter.__str__())
            line = fd.readline()
            counter += 1
        fd.close()
    except IOError:
        pass

def start_task(task, params):
    if task == 'NEW_LINE':
        str=params[0]
        #fd = open(params[0])
        #str = fd.readline()
        #while(len(str) != 0):
        str = str.replace('\n', '')
        path_from = params[1]
        path_to = params[2]
        add_new_line(str, path_from, path_to,  params[3])
            #str = fd.readline()
        #fd.close()
    elif task == 'PRINT_EMP':
        fd = open(params[0])
        str = fd.readline()
        to_find = list()
        while(len(str) != 0):
            str = str.replace('\n', '')
            to_find.append(str)
            str = fd.readline()
        fd.close()
        if len(to_find) > 0:
            print_emp_to_process(params[1],params[2], to_find)
