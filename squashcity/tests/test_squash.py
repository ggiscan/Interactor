'''
Created on Sep 23, 2015

@author: george
'''
import unittest
from core.tests.common import Message
from squashcity.squash_command import SquashCity
from core.server import CommandServer
from core.commons import success, Context
import core.dbman as dbman

class TestSquash(unittest.TestCase):
    def setUp(self):
        s = success()
        self.messages = [#starting on Thursday until Friday between 19-21
                    ('THU FRI 19:00 21:00', s),
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
        
    def test_squash(self):
        session = dbman.new_session("memory")
        dbman.create_product("SquashCity", session)
        dbman.register_user("SquashCity", "George", session)
        
        s = success()
        server = CommandServer([Message(i, 'CMD SquashCity ' + msg[0], 'George') 
                                for (i,msg) in enumerate(self.messages)]) 
        #print list(server)
        context = Context(session)
        for (i,c) in enumerate(list(server)):
            if isinstance(c, Exception):
                self.assertEqual(c.message, self.messages[i][1])
            else:
                res = c.execute(context)
                self.assertEqual(s, res)
                    