'''
Created on Nov 15, 2015

@author: george
'''
from core.model import Request
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from datetime import datetime

class SquashCityRequest(Request):
    __tablename__ = 'squash_request'
    id = Column(Integer, ForeignKey('request.id'), primary_key=True)
    start_date = Column(DateTime,  default=datetime.utcnow)
    end_date = Column(DateTime,  default=datetime.utcnow)
    __mapper_args__ = {
        'polymorphic_identity':'SQUASHCITY'
    } 
       
    def __repr__(self):
        return '<SquashCityRequest({id}, {start_date}, {end_date}>'.format(**self.__dict__)
    