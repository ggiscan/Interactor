'''
Created on Sep 21, 2015

@author: george
'''
import unittest
from core import dbman
from core import commons as com
from core.model import User

class TestDBMan(unittest.TestCase):
        def setUp(self):
            self.session = dbman.new_session('memory')
            self.username = "george"
            self.products = ['product1', 'product2']
                
        def test_all(self):
            self.create_user_invalid_product()
            self.create_user()
            self.query_user_product()
            
        def create_user_invalid_product(self):
            result = dbman.register_user('DUMMY_CATEG', self.username, session=self.session)
            self.assertEqual(com.error(com.ERR_INVALID_PRODUCT), result)
            
        def create_user(self):
            #create a category
            res = dbman.create_product(self.products[0], session=self.session)
            self.assertEqual(com.success(), res)
            
            #create a user assigned to that category
            res = dbman.register_user(self.products[0], self.username, session=self.session)
            self.assertEqual(com.success(), res)
            
            #create the user again
            res = dbman.register_user(self.products[0], self.username, session=self.session)
            self.assertEqual(com.error(com.WARN_ALREADY_REGISTERED), res)
            
            #create another category
            res = dbman.create_product(self.products[1], session=self.session)           
            self.assertEqual(com.success(), res)
            
            #assign existing user to another category
            res = dbman.register_user(self.products[1], self.username, session=self.session)
            self.assertEqual(com.success(), res)
                       
        def query_user_product(self):
            u = self.session.query(User).filter(User.id==self.username).one()
            self.assertEqual([p.upper() for p in self.products], [p.id for p in u.products])
            
            self.assertEqual([up for up in u.user_products], 
                             [dbman.query_user_product(self.username, p, session=self.session) 
                              for p in self.products])

                                       
#if __name__ == '__main__':
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestDBMan)
#    unittest.TextTestRunner(verbosity=2).run(suite)
