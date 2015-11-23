'''
Created on Sep 21, 2015

@author: george
'''
from model import User, Product, UserProduct, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
import commons as com
from collections import namedtuple

options_type = namedtuple('options', ['create_db', 'conn_string', 'echo', 'engine'])
OPTIONS={'live' : options_type(False, 'sqlite:///db/sqlite.db', False, None),
         'live_create_once' : options_type(True, 'sqlite:///db/sqlite.db', False, None),
         'memory' : options_type(True, 'sqlite:///:memory:', True, None)}

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
    return sessionmaker(bind=engine)()

def register_user(product_name, user_name, session):
    '''Create (if it doesn't exist yet) and register (if not already registered)
    the user_name to the product_name
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
        user.products.append(prod)
        session.add(user)
        session.commit()
        return com.success()
    except NoResultFound:
        return com.error(com.ERR_INVALID_PRODUCT)

def query_user_product(user_name, product_name, session):
    '''Return a UserProduct object for product_name and user_name if found,
       otherwise return None
    '''
    try:
        #check that the product exists - must be created by the admin
        user_product = (session.query(UserProduct).join(User).join(Product).
                         filter(User.id==user_name, Product.id==product_name.upper()).one())
        return user_product
    except NoResultFound:
        return None
    
def create_product(product_name, session):
    product_name = product_name.upper()
    products = session.query(Product).filter(Product.id==product_name).all()
    if len(products):
        return com.error(com.WARN_EXISTING_CATEGORY)
    else:
        p = Product(id = product_name)
        session.add(p)
        session.commit()
    return com.success()
