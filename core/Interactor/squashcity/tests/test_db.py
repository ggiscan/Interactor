'''
Created on Nov 19, 2015

@author: george
'''
import unittest
from core.model import User
import core.dbman as dbman
from squashcity.model import SquashCityRequest
import sys
from datetime import datetime

class TestDBModel(unittest.TestCase):
    def setUp(self):
        self.session = dbman.new_session('memory')
        self.product = 'SQUASHCITY'
        self.user = 'George'
        
    def test_squash(self):
        self.create_users_and_products()
        self.create_requests()
        self.active_product_requests()
        self.active_user_requests()
        
    def create_users_and_products(self):
        dbman.create_product(self.product, self.session)
        dbman.register_user(self.product, self.user, session=self.session)
        
    def create_requests(self):
        session = self.session
        try:
            user = session.query(User).filter(User.id==self.user).one()
            user_product = user.user_products[0]
            #below request is active
            squashcity_req = SquashCityRequest(request_type=self.product, 
                                               userproduct_id = user_product.id,
                                               start_date = datetime.now(),
                                               end_date = datetime(2015, 11, 5, 22, 36))
            session.add(squashcity_req)
            #below request is inactive
            squashcity_req = SquashCityRequest(request_type=self.product, 
                                               userproduct_id = user_product.id,
                                               closing_date = datetime.now(),
                                               start_date = datetime.now(),
                                               end_date = None)
            session.add(squashcity_req)
            session.commit()
        except:
            self.assertTrue(False, sys.exc_info()[1])
            
    def active_product_requests(self):
        requests = dbman.active_product_requests(self.product, session=self.session)
        self.assertEqual(1, len(requests))
        self.assertIsNone(requests[0].closing_date)
        
    def active_user_requests(self):
        requests = dbman.active_user_requests(self.user, self.product, session=self.session)
        self.assertEqual(1, len(requests))
        self.assertIsNone(requests[0].closing_date)
        