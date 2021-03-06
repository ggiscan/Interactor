'''
Created on Sep 18, 2015

@author: george
'''
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey,func
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from datetime import datetime

date_sentinel = datetime(2000,1,1)
Base = declarative_base()
class User(Base):
    __tablename__ = 'user'
    id = Column(String, primary_key=True)
    password = Column(String)
    active = Column(Boolean, default=False)
    creation_date = Column(DateTime, default=func.now())
    products = relationship('Product', secondary='user_product_link')
    user_products = relationship('UserProduct', cascade="all, delete-orphan", backref=backref('user'))
    def __repr__(self):
        return ("<User({id}, {password}, {active}, {creation_date})>" 
                .format(**self.__dict__))

class Product(Base):
    __tablename__ = 'product'
    id = Column(String, primary_key=True)
    users = relationship(User, secondary='user_product_link')
    user_products = relationship('UserProduct', cascade="all, delete-orphan", backref=backref('product'))     
    def __repr__(self):
        return "<Product({})>".format(self.id)

class UserProduct(Base):
    __tablename__ = 'user_product_link'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('user.id'))
    product_id = Column(String, ForeignKey('product.id'))
    requests = relationship('Request', cascade="all, delete-orphan", backref=backref('user_product'))
    priority = Column(Integer, default=None)
    def __repr__(self):
        return ("<UserProduct(user_id={},product_id={})>" 
                .format(self.user.id, self.product.id))

class Request(Base):
    __tablename__ = 'request'
    id = Column(Integer, primary_key=True)
    request_type = Column(String)
    userproduct_id = Column(String, ForeignKey('user_product_link.id'))
    creation_date = Column(DateTime, default=func.now())
    closing_date = Column(DateTime, default=None)
    priority = Column(Integer, default=None)
    __mapper_args__ = {
        'polymorphic_on' : request_type
    }

    def __repr__(self):
        return ('<Request({id}, {user_id}, {product_id}, '
               '{creation_date}, {closing_date})>'.format(**self.__dict__))

