'''
Created on Sep 23, 2015

@author: george
'''
#command('SQUASH')
from datetime import datetime, time
from squashcity.model import SquashCityRequest
from core.registry import command
from core.commons import success, retry_later, user_not_registered
from core.dbman import query_user_product
import re
import logging
import utils
import sys

regex_weekday = '|'.join(utils._WEEKDAYS)
regex_hour = '({0})(?::({0}))?'.format('[0-9]{1,2}')
regex = r'({0})?({0})?(?:{1})?(?:{1})?'.format(regex_weekday, regex_hour)
pat = re.compile(regex)

@command('SquashCity')
class SquashCity:
    def __init__(self, *args, **kwargs):
        '''
        Create a schedule for SquashCity
        Expect the command in the following format:
        [DAYNAME_START] [DAYNAME_END] [TIME_START] [TIME_END]
        If DAYNAME_START is missing it is defaulted to today
        If DAYNAME_END is missing it is defaulted to today
        If TIME_START is missing it is defaulted to now()
        If TIME_END is missing it is defaulted to 23:59
        
        The SquashCity schedule is processed by the squashcity daemon 
        '''
        self.username = kwargs['username']
        args = ''.join(args)
        match = re.match(pat, args)
        if not match:
            raise ValueError('Squash - incorrect parameters')
        from_day, to_day, from_time_h, = match.groups()[:3]
        from_time_m, to_time_h, to_time_m = match.groups()[3:]
        if to_day == None: to_day = from_day
        if from_time_h == None:
            tm_now = datetime.now().time()
            from_time_h, from_time_m = tm_now.hour, tm_now.minute
        if to_time_h == None:
            to_time_h = 23
            to_time_m = 59
        if from_time_m == None: from_time_m=0
        if to_time_m == None: to_time_m = 0
        from_time_h, from_time_m = int(from_time_h), int(from_time_m)
        to_time_h, to_time_m = int(to_time_h), int(to_time_m)
        try:
            _ = time(from_time_h, from_time_m)
            _ = time(to_time_h, to_time_m)
        except ValueError:
            raise ValueError('Squash - incorrect parameters')
        d_from = utils.date_from_string(from_day, from_time_h, from_time_m)
        d_to = utils.date_from_string(to_day,
                                      reference_day=d_from, 
                                      hour=to_time_h, 
                                      minute=to_time_m)
        if d_from > d_to:
            raise ValueError("Squash - start date greater than end date")
        self.d_from, self.d_to = d_from, d_to
        
    def execute(self, context):
        logging.info('Creating squash schedule for user ', self.username)
        session = context.session
        try:
            user_product = query_user_product(self.username, 'squashcity', session)
            if user_product is None:
                return user_not_registered()
            squashcity_req = SquashCityRequest(request_type = 'SQUASHCITY',
                                               user_product=user_product,
                                               priority = user_product.priority,
                                               start_date=self.d_from,
                                               end_date=self.d_to)
            
            session.add(squashcity_req)
            session.commit()
            return success()
        except:
            print "Exception in SquashCity.execute: ", sys.exc_info()
            return retry_later()
 
if __name__ == '__main__':
    pass