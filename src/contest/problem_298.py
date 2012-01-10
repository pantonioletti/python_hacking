'''
Created on Jul 22, 2010

@author: pantonio
'''
from sys import argv
from random import seed
from random import randint
from math import fabs
from threading import Thread
from time import sleep
import threading

class Multi_th_counter:
    def __init__(self, val, lock):
        self.counter=int(val)
        self.lock = lock
    def downward(self, val):
        ret = False
        if self.counter > 0:
            ret=True
            self.lock.acquire()
            self.counter -= val
            self.lock.release()
        return ret
            
        
class Sol_Thread(Thread):
    def __init__(self, pname, counter):
        Thread.__init__(self)
        self.name = pname
        self.sol = 0.0
        self.times=0.0
        self.cycles = 100
        self.counter = counter
    
    def run(self):
        while self.counter.downward(self.cycles):
            for i in range(self.cycles):
                self.sol += fabs(solution())
            self.times += self.cycles

def multi_th_sol(num_th, cycles):
    th_list = list()
    l = threading.Lock()
    counter = Multi_th_counter(cycles, l)
    for i in range(int(num_th)):
        thread = Sol_Thread(i, counter)
        thread.start()
        th_list.append(thread)
    all_running = True
    while all_running:
        alive = 0
        for i in range(len(th_list)):
            if th_list[i].is_alive():
                alive += 1
                break
        all_running = alive > 0
        sleep(5)
        print("Current counter value: " + counter.counter.__str__())
    th_cycles = 0
    th_sum = 0
    for i in range(len(th_list)):
        th_sum += th_list[i].sol
        th_cycles += th_list[i].times
    print(th_cycles)
    print(th_sum)
    print(th_sum/th_cycles)
    
                
class num_status:
    def __init__(self):
        self.last = 0
        self.start = 0

def solution():
    seed()
    l_score = 0
    r_score = 0
    
    l_buffer = list()
    l_num_status = dict()
    r_buffer = list()
    r_num_status = dict()
    for i in range(50):
        num = randint(1,10)
        if num in l_buffer:
            l_score += 1
            l_num_status[num].last = i
        else:
            if len(l_buffer) == 5:
                last = l_num_status[l_buffer[0]].last
                to_rm = l_buffer[0]
                for j in range(1,4):
                    if last > l_num_status[l_buffer[j]].last:
                        last = l_num_status[l_buffer[j]].last
                        to_rm = l_buffer[j]
                l_buffer.remove(to_rm)
                l_num_status.pop(to_rm)
            stat = num_status()
            stat.last = i
            l_num_status[num] = stat
            l_buffer.append(num)
        if num in r_buffer:
            r_score += 1
        else:
            if len(r_buffer) == 5:
                to_rm = r_buffer.pop(0)
                r_num_status.pop(to_rm)
            r_buffer.append(num)
            stat = num_status()
            stat.start = i
            r_num_status[num] = stat
    return(l_score-r_score)
    
if argv[1] == "MT":
    threads = argv[2]
    cycles = argv[3]
    multi_th_sol(threads, cycles)
else:
    sum = 0.0
    for i in range(10000000):
        sum += fabs(solution())
    print(sum)
    print(sum/10000000.0)