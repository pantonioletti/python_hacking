'''
Created on 29-05-2009
You are given the following information, but you may prefer to do some research for yourself.

1 Jan 1900 was a Monday.
Thirty days has September, April, June and November.
All the rest have thirty-one,
Saving February alone,
Which has twenty-eight, rain or shine.
And on leap years, twenty-nine.
A leap year occurs on any year evenly divisible by 4, but not on a century unless 
it is divisible by 400. How many Sundays fell on the first of the month during the 
twentieth century (1 Jan 1901 to 31 Dec 2000)?
@author: pantonio
'''
def is_leap_year(year):
    cd = year%400
    c = year%100
    iv = year%4
    is_leap = False
    if (iv == 0 and (c > 0 or cd == 0)):
        is_leap = True
    return is_leap 

def problem19():
    month_days = {1: 31, 2: 28, 3: 31, 4: 30, 
                  5: 31, 6: 30, 7: 31, 8: 31, 
                  9: 30, 10: 31, 11: 30, 12: 31}
    week_days = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}
    start_date = [1, 1, 1900]
    end_date = [31,12,2000]
    days = 0
    sundays = 0
    while(start_date != end_date):
        if (start_date[2] > 1900 and ((days%7)+1) == 7):
            sundays += 1
        if (start_date[1] == end_date[1] and start_date[2] == end_date[2]):
            days += end_date[0] - (start_date[0])
            start_date[0] = end_date[0]
        else:
            aux_days = month_days[start_date[1]] - (start_date[0]-1)
            if (start_date[1] == 2):
                if (is_leap_year(start_date[2])):
                    aux_days += 1
            days += aux_days
            start_date[0]=1
            start_date[1]+=1
            if (start_date[1] > 12):
                start_date[1] = 1
                start_date[2] += 1
    day_of_week = days % 7
    print(sundays.__str__() + "\n")
    #print(week_days[day_of_week+1])

problem19()         
