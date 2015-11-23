'''
Created on Sep 14, 2015

@author: george
'''
class MemoryDS:
    def __init__(self, messages):
        self._messages = messages
        
    def __iter__(self):
        return [m for m in self._messages]

class Message:
    def __init__(self, aid, text, username):
        self.id = aid
        self.text = text
        self.username = username
        self.data_source = 'memory'
