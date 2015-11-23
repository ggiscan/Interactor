'''
Created on Nov 19, 2015

@author: george
'''
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.model import Base, UserProduct
from core.dbman import create_database, create_product, create_user
from model import SquashCityRequest

from datetime import datetime

class TestDBModel(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()
    
    def test_squash(self):
        
    def create_requests(self):
        session = self.session
        user_product = session.query(UserProduct).filter(UserProduct.user_id == 'TestUser1', 
                                                         UserProduct.product_id == 'SQUASHCITY').one()
        end_date = datetime(2015, 11, 5, 22, 36)
        squashcity_req = SquashCityRequest(user_id = user_product.user_id, 
                                           product_id = user_product.product_id,
                                           start_date = datetime.now(),
                                           end_date = end_date)
        session.add(squashcity_req)
        session.commit()
        squashcity_req = session.query(Request).filter(Request.user_id == 'TestUser1').one()
        self.assertEqual(end_date, squashcity_req.end_date)