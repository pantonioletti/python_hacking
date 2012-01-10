import math
import threading
import time
'''
Created on 29-05-2009
Let us call an integer sided triangle with sides a  b  c 
barely acute if the sides satisfy 
 a**2 + b**2 = c**2 + 1.

How many barely acute triangles are there with 
perimeter <= 25,000,000?
@author: pantonio
'''
barely_acute = [0]
value = [12500000]
inc_lock = [None]
get_lock = [None]

class MyThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
        
    def run(self):
        c = get_c()
        while(c > 0):
            cp2 = c ** 2
            a = 1
            b = c
            count = 0
            while(a < b):
                sum = b**2 + a**2
                while(sum -1 < cp2):
                    a =+ 1
                    sum = b**2 + a**2
                if (sum - cp2 == 1):
                    if (a + b + c <25000001):
                        count += 1
                b -= 1
            count *= 2
            sum = b**2 + a**2
            if (sum - cp2 == 1):
                if (a + b + c <25000001):
                    count += 1
            inc(count)     
            c = get_c()

def counter_test(p):
#    c = p**2
    pass
    for x in range(1, p):
        #c = x**2
        #d = x**2
        e = math.sqrt(x**2 + x**2) - p#c + d
        
def get_c():
    get_lock[0].acquire()
    ret_val = value[0]
    value[0] -= 1
    get_lock[0].release()
    return ret_val

def inc(val):
    inc_lock[0].acquire()
    barely_acute[0] += val
    inc_lock[0].release()
def p():
    print("Actual count : " + barely_acute[0].__str__()+ " | actual c value : " + value[0].__str__())
def problem223(th):
    still_run = True
    while(still_run):
        t = threading.Timer(30,p)
        t.start()
        t.join()
        still_run = False
        for i in range(len(th)):
            if (th[i].is_alive()):
                still_run = True
                break
    
def start():
    threads = 2
    inc_lock[0] = threading.Lock()
    get_lock[0] = threading.Lock()
    t = dict()
    for x in range(threads):
        t[x] = MyThread(x.__str__())
        t[x].start()
        
    problem223(t)
    p()
def test():
    rep = 3
    for i in range(rep):
        print("I : " + i.__str__() + "\n")
#===============================================================================
#    val = 100000
#    rep = 3
#    x = time.time()
#    y = 0
#    for i in range(0, rep):
#        print("I : " + i.__str__() + "\n")
#        y += 1
#        counter_test(val)
#    x = time.time() - x
#    m = x/rep
#    print("Y : " + y.__str__() + "\n")
#    print("Average time : " + m.__str__())
#===============================================================================

start()
#test()