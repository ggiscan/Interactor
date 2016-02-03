'''
Created on Nov 15, 2015

@author: george
'''
from core.model import Request
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func

class SquashCityRequest(Request):
    __tablename__ = 'squash_request'
    id = Column(Integer, ForeignKey('request.id'), primary_key=True)
    start_date = Column(DateTime,  default=func.now())
    end_date = Column(DateTime,  default=func.now())
    found_court = Column(Integer, default=None)
    found_date = Column(DateTime, default=None)
    __mapper_args__ = {
        'polymorphic_identity':'SQUASHCITY'
    } 
    
    def close(self, match):
        self.found_court = match.court
        self.found_date = match.start_date
        
    def __contains__(self, avlb_date):
        '''
        Check if a (dt_start, dt_end) date tuple is contained in the 
        start_date, end_date interval
        The semantics of start_date, end_date is as follows:
        everyday from day(start_date) to day(end_date)
        between time(start_end) and time(end_date)
        '''   
        dt_start, dt_end = avlb_date
        req_start_date, req_start_time = self.start_date.date(), self.start_date.time()
        req_end_date, req_end_time = self.end_date.date(), self.end_date.time()
        if not (req_start_date <= dt_start.date() <= req_end_date):
            return False
        if not (req_start_time <= dt_start.time() < dt_end.time() <= req_end_time):
            return False
        return True
    
    def __repr__(self):
        #force sql-alchemy load
        _ = self.start_date
        return '<SquashCityRequest({id}, {start_date}, {end_date}>'.format(**self.__dict__)
    