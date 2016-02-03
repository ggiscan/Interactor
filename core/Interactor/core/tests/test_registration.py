'''
Created on Sep 14, 2015

@author: george
'''
import unittest
import sys

from common import Message
from core.server import CommandServer
from core.commands import Register
from core.dbman import new_session, create_product

class TestRegistration(unittest.TestCase):
    def setUp(self):
        self.session = new_session('memory')
        message = Message(1, 'CMD Register Squash', '@George')
        server = CommandServer([message])
        self.command = [c for c in server][0]
    
    def test_registration(self):
        create_product("squash", self.session)
        ret_code,_ = self.command.execute()
        self.assertEqual(0, ret_code)
        ret_code,message = self.command.execute()
        self.assertEqual('Already registered for this product', message)
        