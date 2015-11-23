'''
Created on Sep 21, 2015

@author: george
'''
import unittest
from core import dbman
from core import commons as com

class TestDBMan(unittest.TestCase):
        def setUp(self):
            self.session = dbman.new_session('memory')

        def test_create_user_invalid_product(self):
            result = dbman.register_user('DUMMY_CATEG', 'testusergeorge', self.session)
            self.assertEqual(com.error(com.ERR_INVALID_PRODUCT), result)
            
        def test_create_user(self):
            #create a category
            categ_name = 'TESTDBMAN.PRODUCT1'
            res = dbman.create_product(categ_name, self.session)
            self.assertEqual(0, res.code)
            
            #create a user assigned to that category
            res = dbman.register_user(categ_name, 'testusergeorge', self.session)
            self.assertEqual(0, res.code)
            
            #create the user again
            res = dbman.register_user(categ_name, 'testusergeorge', self.session)
            self.assertEqual(com.error(com.WARN_ALREADY_REGISTERED), res)
            
            #create another category
            categ_name = 'TESTDBMAN.PRODUCT2'
            res = dbman.create_product(categ_name, self.session)           
            self.assertEqual(0, res.code)
            
            #assign existing user to another categimportory
            res = dbman.register_user(categ_name, 'testusergeorge', self.session)
            self.assertEqual(0, res.code)
                                    
#if __name__ == '__main__':
#    suite = unittest.TestLoader().loadTestsFromTestCase(TestDBMan)
#    unittest.TextTestRunner(verbosity=2).run(suite)
