'''
Created on 2 Dec 2015

@author: ggiscan
'''
from collections import namedtuple

def test_fun(a):
    print 'a=',a

test_type = namedtuple("test_type","court start_date end_date")
    
if __name__ == '__main__':
    t1=test_type(9, *(0, 1))
    print t1
