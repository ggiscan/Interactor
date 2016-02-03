'''
Created on Sep 18, 2015

@author: george
'''
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.model import User, Product, Base, UserProduct

class TestDBModel(unittest.TestCase):
    def setUp(self):
        engine = create_engine('sqlite:///:memory:', echo=True)
        Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()
    
    def test_everything(self):
        self.create_users_and_products()
        
    def create_users_and_products(self):
        '''
         Create a dummy user and persist it.
         Fetch it from the database and verify that the identity map holds
         Check that the id is created
        '''
        
        session = self.session
        user1 = User(id = "TestUser1", password = "TestPass")
        user2 = User(id = "TestUser2", password = "TestPass")
        products = [Product(id=_id) for _id in ["SQUASHCITY", "SUBTITLES"]]
        prod_user1, prod_user2 = products, products[1:]  
        user1.products.extend(prod_user1)
        user2.products.extend(prod_user2)
        session.add(user1)
        session.add(user2)
        session.commit()
        q_products = [user_prod.product for user_prod in session.query(UserProduct)
                     .join(User)
                    .filter(User.id == "TestUser1")
                    .order_by(UserProduct.product_id).all()]
        self.assertEqual(prod_user1, q_products)
        q_products = [user_prod.product for user_prod in session.query(UserProduct)
                    .join(User)
                    .filter(User.id == "TestUser2")
                    .order_by(UserProduct.product_id).all()]
        self.assertEqual(prod_user2, q_products)
    

