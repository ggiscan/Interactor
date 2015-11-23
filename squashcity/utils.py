'''
Created on Nov 22, 2015

@author: george
'''
from datetime import datetime,timedelta
_WEEKDAYS = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

def nextday_byname(day_name, start_date = None):
    '''
    Return a date object representing the date of the next occurrence
     of day_name
    '''
    if not day_name in _WEEKDAYS:
        return None
    if start_date is None:
        start_date = datetime.today()
        start_date = start_date - timedelta(hours = start_date.hour, 
                                            minutes = start_date.minute, 
                                            seconds = start_date.second )
    day_num = start_date.weekday()
    day_num_target = _WEEKDAYS.index(day_name)
    day_delta = (7 + day_num_target - day_num) % 7
    if day_delta == 0: day_delta = 7
    end_date = start_date + timedelta(days=day_delta)
    return end_date

def date_from_string(dayname, hour, minute):
    '''Find the next date for dayname, hour, minute,
    transform to date format then return the result in SQL format
    '''
    if hour == None:
        hour = 0 
    if minute == None:
        minute = 0 
    if not dayname:
        start_date = datetime.today()
        start_date = start_date - timedelta(hours = start_date.hour, 
                                            minutes = start_date.minute, 
                                            seconds = start_date.second )
    else:
        start_date = nextday_byname(dayname)
    start_date += timedelta(hours = int(hour),
                            minutes = int(minute)) 
    return start_date
