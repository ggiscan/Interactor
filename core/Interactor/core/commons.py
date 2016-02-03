'''
Created on 4 Apr 2014

@author: geo
'''
from collections import namedtuple
import logging

error_type = namedtuple('error', ['code', 'message'])
(ERR_INVALID_PRODUCT,
WARN_ALREADY_REGISTERED,
WARN_EXISTING_CATEGORY,
ERR_USERNOTREGISTERED,
ERR_RETRY_LATER) = range(400,405)

ERROR_MESSAGES = {ERR_INVALID_PRODUCT:      'Invalid product for registration',
                  WARN_ALREADY_REGISTERED:  'Already registered for this product',
                  WARN_EXISTING_CATEGORY:   'The category is already created',
                  ERR_USERNOTREGISTERED:    'The user is not registered for product {}',
                  ERR_RETRY_LATER: 'Unable to process your request at this time. Please try again later'}

def user_not_registered():
    return error(ERR_USERNOTREGISTERED)

def retry_later():
    return error(ERR_RETRY_LATER)

def success():
    return error_type(0, "Success")

def error(error_code):
    return error_type(error_code, ERROR_MESSAGES[error_code])

def feedback(message):
    print "Feedback to be implemented: %s" % message
    return message

class Context:
    def __init__(self, session):
        self.session = session

def init_logging():
    logging.basicConfig(filename='global.log', 
                        format='%(asctime)s %(levelname)s %(message)s:', 
                        level=logging.DEBUG)
