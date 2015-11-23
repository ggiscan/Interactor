'''
Created on Nov 20, 2015

@author: george
'''
import twitter
import shelve

SHELVE_NAME, LAST_MESSAGE_KEY = 'cached_data', 'lastMessageId'
 
class TwitDataSource:
    def __init__(self):
        self._api = twitter.Api(consumer_key='tjxnkM9t4JbNvSh7TO3aUg',
                                consumer_secret='OnTZSA0NhhVybiq2zdXHLoq7RJrQXq65lQS0qRa5so',
                                access_token_key='2440736637-Lnaw5RPvurpdCQiMZLw322IQbk4sjuhxZI8aUKU',
                                access_token_secret='BRzdLDEHm1wuJezU7fOD5RNF41sZv1M47SHqKqBr49KHY')
    
    def __iter__(self):
        '''Return the last direct messages received by the account
           Use a shelve cache to keep the id of the last read message
           Upon retrieval of new messages updates the cache'''
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