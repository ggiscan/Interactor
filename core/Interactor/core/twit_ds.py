'''
Created on Nov 20, 2015

@author: george
'''
try:
    import twitter
except ImportError:
    print "***Unable to import twitter module: not installed or not in PYTHONPATH"
import shelve
import os 

SHELVE_NAME, LAST_MESSAGE_KEY = 'cached_data', 'lastMessageId'
 
class TwitDataSource:
    def __init__(self):
        self._api = twitter.Api(os.environ['consumer_key'],
                                os.environ['consumer_secret'],
                                os.environ['access_token_key'],
                                os.environ['access_token_secret'])
    
    def __iter__(self):
        '''Return the last direct messages received by the account
           Use a shelve cache to keep the id of the last read message
           Upon retrieval of new messages updates the cache
        '''
        try:
            cache = shelve.open(self._shelve_name)
            last_mess_id = cache[LAST_MESSAGE_KEY]
        except KeyError:
            last_mess_id = None
        res = [TwitMessage(m) for m in self._api.GetDirectMessages(since_id = last_mess_id)]
        cache[LAST_MESSAGE_KEY] = res[-1].id
        cache.close()
        return res
    
    def __repr__(self):
        return "<TwitDataSource>"

class TwitMessage:
    def __init__(self, msg):
        self._msg = msg
        
    def __getattr__(self, attr):
        if attr == 'username':
            return self._msg.sender_screen_name
        else:
            return self.__getattr__(attr)
        
    def __repr__(self):
        return "<TwitMessage(message={message}, username={username})".format(self.__dict__)

if __name__ == '__main__':
    pass