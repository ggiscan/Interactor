'''
Created on Sep 21, 2015

@author: george
'''
from model import User, Product, UserProduct, Base
from sqlalchemy import create_engine,func
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound
import commons as com
from collections import namedtuple
from itertools import chain
import os

DB_CONNECTION = 'sqlite:///' + os.path.join(os.path.dirname(__file__), 'db', 'interactor.db')
options_type = namedtuple('options', ['create_db', 'conn_string', 'echo', 'engine'])
OPTIONS={'live' : options_type(False, DB_CONNECTION, True, None),
         'live_create_once' : options_type(True, DB_CONNECTION, False, None),
         'memory' : options_type(True, 'sqlite:///:memory:', False, None)}

Session = scoped_session(sessionmaker())

def new_session(data_source):
    global OPTIONS
    opts = OPTIONS[data_source]
    engine = opts.engine
    if engine is None:
        engine = create_engine(opts.conn_string, echo=opts.echo)
        if opts.create_db:
            Base.metadata.create_all(engine)
        OPTIONS[data_source] = options_type(opts.create_db, 
                                            opts.conn_string, 
                                            opts.echo, 
                                            engine)
        Session.configure(bind=engine)
    return Session()

def register_user(product_name, user_name, priority=None, session=None):
    '''
    Create and register the user_name to the product_name
    '''
    try:
        #check that the product exists - must be created by the admin
        product_name = product_name.upper()
        prod = session.query(Product).filter(Product.id==product_name).one()
        users = prod.users
        if user_name in [u.id for u in users]:
            return com.error(com.WARN_ALREADY_REGISTERED)
        users = session.query(User).filter(User.id==user_name).all()
        if len(users):
            user = users[0]
        else:
            user = User(id=user_name, password="")
        user.products.append(prod)
        session.add(user)
        session.commit()
        return com.success()
    except NoResultFound:
        return com.error(com.ERR_INVALID_PRODUCT)
    
def register_user_old(product_name, user_name, priority=None, session=None):
    '''
    Create and register the user_name to the product_name
    '''
    try:
        #check that the product exists - must be created by the admin
        product_name = product_name.upper()
        prod = session.query(Product).filter(Product.id==product_name).one()
        
        user_products = session.query(UserProduct).join(User).filter(User.id==user_name).all()
        if len(user_products):
            #check if the user is already subscribed to this product
            if product_name in [p.product.id for p in user_products]:
                return com.error(com.WARN_ALREADY_REGISTERED)
            #the user exists but is not registered to this category
            user = user_products[0].user
        else:
            #the user does not exist - create it
            user = User(id=user_name, password="")
        up = UserProduct(user=user, product=prod, priority=priority)
        user.user_products.append(up)
        session.add(user)
        session.commit()
        return com.success()
    except NoResultFound:
        return com.error(com.ERR_INVALID_PRODUCT)

def query_user_product(user_name, product_name, session=None):
    '''
    Return a UserProduct object for user_name and product_name if found,
    otherwise return None
    '''
    try:
        #check that the product exists - must be created by the admin
        user_product = (session.query(UserProduct).join(User).join(Product)
                        .filter(User.id==user_name, Product.id==product_name.upper()).one())
        return user_product
    except NoResultFound:
        return None

def active_user_requests(user_name, product_name, session=None):
    '''
    Return a list of Requests object for user_name and product_name
    only considering the 'active' requests, i.e closing_date is None
    '''
    up = query_user_product(user_name, product_name, session)
    if up is None:
        return []
    return [r for r in up.requests if r.closing_date is None]

def active_product_requests(product_name, session=None):
    '''
    Return a list of Requests object for user_name and product_name
    only considering the 'active' requests, i.e closing_date is None
    '''
    try:
        p = session.query(Product).filter(Product.id==product_name.upper()).one()
        requests = chain(*[up.requests for up in p.user_products])
        return [r for r in requests if r.closing_date is None]
    except NoResultFound:
        return []

def close_requests(matched_requests, session=None):
    for (request, match) in matched_requests.items():
        request.close(match)
        request.closing_date = func.now()
        session.add(request)
    session.commit()

def create_product(product_name, session=None):
    product_name = product_name.upper()
    products = session.query(Product).filter(Product.id==product_name).all()
    if len(products):
        return com.error(com.WARN_EXISTING_CATEGORY)
    else:
        p = Product(id = product_name)
        session.add(p)
        session.commit()
    return com.success()

