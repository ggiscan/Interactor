'''
Created on Sep 23, 2015

@author: george
'''
import unittest
from core.tests.common import Message
from squashcity.squash_cmd import SquashCity
from core.server import CommandServer
from core.commons import success, Context
import core.dbman as dbman
from squashcity.utils import date_from_string

class TestSquash(unittest.TestCase):
    def setUp(self):
        s = success()
        self.messages = [#starting on Thursday until Friday between 19-21
                    ('WED FRI 19:00 21:00', s),
                    #starting today until next Friday between 19-21
                    ('FRI 19 21', s),
                    #starting today until next Friday after 19
                    ('FRI 19', s),
                    #only today 19 - 21
                    ('19 21', s),
                    #only today after 19
                    ('19', s),
                    #today starting now
                    ('', s), 
                    ('17:30 16:30', 'Squash - start date greater than end date'),
                    ('29:5', 'Squash - incorrect parameters')
                    ]
        self.session = dbman.new_session("memory")

        
    def test_squash(self):
        self.validate_commands()
        self.check_active()
        
    def validate_commands(self):
        dbman.create_product("SquashCity", session=self.session)
        dbman.register_user("SquashCity", "George", session=self.session)
        
        s = success()
        server = CommandServer([Message(i, 'CMD SquashCity ' + msg[0], 'George') 
                                for (i,msg) in enumerate(self.messages)]) 
        #print list(server)
        context = Context(self.session)
        for (i,c) in enumerate(list(server)):
            if isinstance(c, Exception):
                self.assertEqual(c.message, self.messages[i][1])
            else:
                res = c.execute(context)
                self.assertEqual(s, res)
                
    def check_active(self):
        active = dbman.active_product_requests('squashcity', session=self.session)
        self.assertEqual(6, len(active))
        'THU FRI 19:00 21:00'
        req = active[0]
        ds,de = date_from_string('THU', 19, 0), date_from_string('THU', 19, 45)
        self.assertTrue((ds,de) in req)
        ds = date_from_string('THU', 18, 45)
        self.assertFalse((ds,de) in req)
        ds, de = date_from_string('THU', 20, 30), date_from_string('THU', 21, 15)
        self.assertFalse((ds,de) in req)
        ds, de = date_from_string('SAT', 19, 0), date_from_string('SAT', 19, 45)
        self.assertFalse((ds,de) in req)
        
        
