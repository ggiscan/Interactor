'''
Created on Nov 22, 2015

@author: george
'''
import datetime as dt
_WEEKDAYS = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']

def nextday_byname(day_name, start_date=None):
    '''
    Return a date object representing the date of the next occurrence
     of day_name
    '''
    if not day_name in _WEEKDAYS:
        return None
    if start_date is None:
        start_date = reset_time(dt.datetime.today())
    day_num = start_date.weekday()
    day_num_target = _WEEKDAYS.index(day_name)
    day_delta = (7 + day_num_target - day_num) % 7
    if day_delta == 0: day_delta = 7
    end_date = start_date + dt.timedelta(days=day_delta)
    return end_date

def reset_time(date_time):
    if date_time is None:
        return None
    return dt.datetime.combine(date_time.date(), dt.time())

def date_from_string(dayname, hour=None, minute=None, reference_day=None):
    '''
    Find the next date for dayname, hour, minute,
    starting on reference_day
    '''
    if hour is None:
        hour = 0 
    if minute is None:
        minute = 0 
    if dayname is None:
        start_date = reset_time(dt.datetime.today())
    else:
        start_date = nextday_byname(dayname, reset_time(reference_day))
    start_date += dt.timedelta(hours = int(hour),
                               minutes = int(minute)) 
    return start_date
