'''
Created on 29 Dec 2015

@author: ggiscan
'''
from os import path
import sys

print sys.path

if __name__ == '__main__':
    parent_dir = path.dirname(path.dirname(path.abspath(__file__)))
    print parent_dir
    sys.path.insert(1, parent_dir)
    import WebInteractor
    __package__ = 'WebInteractor'
    from . import app
    app.run()