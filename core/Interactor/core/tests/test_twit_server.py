'''
Created on Sep 10, 2015

@author: george
'''
import unittest
from core.server import CommandServer 
from core.registry import command
from common import Message

class TestTwitServ(unittest.TestCase):
    def setUp(self):
        self._messages = [Message(1, 'CMD Test1', '@George'),
                    Message(2, 'CMD Test2 param1', '@George'),
                    Message(3, 'CMD Test1 param1', '@Ina')]
        self._exp_cmds = [Test1(username = '@George', data_source='memory'),
                    Test2('param1', username = '@George', data_source='memory'),
                    Test1('param1', username = '@Ina', data_source='memory')]   
        
    def test_messages(self):
        twit_stub = self._messages
        server = CommandServer(twit_stub)
        cmds = [c for c in server]
        for i in range(3):
            self.assertEqual(self._exp_cmds[i], cmds[i])
            
        #now we retrieve all the messages again
        cmds = [c for c in server]
        for i in range(3):
            self.assertEqual(self._exp_cmds[i], cmds[i])
            
class Test:
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
    def __eq__(self, other): 
        return self.__dict__ == other.__dict__

@command('Test1')
class Test1(Test):
    pass
@command('Test2')
class Test2(Test):
    pass
if __name__ == '__main__':
    unittest.main()