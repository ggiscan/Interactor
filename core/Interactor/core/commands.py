'''
Created on 31 Mar 2014

@author: geo
'''
from dbman import new_session, register_user
from commons import feedback 
import logging
from registry import command

@command('Register')
class Register:
    def __init__(self, *args, **kwargs):
        self.product = args[0]
        self.username = kwargs['username']
        self.session = new_session(kwargs['data_source'])
        logging.info("Data source: %s", kwargs['data_source'])
        
    def execute(self):
        logging.info("Registering user: %s", self.username)
        (ret_code, message) = register_user(self.product.upper(), self.username, session=self.session)
        feedback(message)
        if not ret_code:
            logging.warn("Could not create the user %s", self.username)
        return ret_code, message

if __name__ == '__main__':
    r = Register('test', username='a', data_source='memory')
    r.execute()
    
