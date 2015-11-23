'''
Created on 30 Mar 2014

@author: geo
'''
import sqlite3 as lite
from datetime import datetime
con = lite.connect('squash.db')
def create_db(recreate=False):
    with con:
        cur = con.cursor()
        if recreate:
            cur.execute('DROP TABLE IF EXISTS categories')
            cur.execute('DROP TABLE IF EXISTS  users')
            cur.execute('DROP TABLE IF EXISTS requests')
        cur.execute('CREATE TABLE categories(cat_name TEXT PRIMARY KEY)')
        cur.execute('INSERT INTO categories VALUES("SQUASH")')
        cur.execute('CREATE TABLE users(user_name TEXT, user_cat TEXT, user_role TEXT, \
                    FOREIGN KEY(user_cat) REFERENCES categories(cat_name))')
        #dates are in the format YYYY-MM-DD HH:MM:SS
        #outcome can be one of 'SUCCESS' or 'CANCELLED'
        #handled flags that this request is currently being handled by a thread/process
        cur.execute('CREATE TABLE IF NOT EXISTS requests(req_user TEXT, req_day_from TEXT, req_day_to TEXT, \
                    req_sched_at TEXT, req_created_at TEXT,req_handled INTEGER, req_outcome TEXT, \
                    FOREIGN KEY(req_user) REFERENCES users(user_name))')

def add_user(username, category):  
    with con:
        cur = con.cursor()
        cur.execute('INSERT INTO users(user_name, user_cat) VALUES(?,?)', (username,category))

def add_request(username, d_from, d_to):
    with con:
        cur = con.cursor()
        now = str(datetime.now()).split(r'.')[0]
        cur.execute('INSERT INTO requests VALUES(?,?,?,?,?,?,?)', (username, d_from, d_to, None, now, 0, None))

def test():
    create_db(True)
    add_user('dummy', 'SQUASH')
    add_request('dummy', '2014-03-30 19:00:00', '2014-03-30 21:00:00')

if __name__ == '__main__':
    test()