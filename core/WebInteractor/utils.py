'''
Created on 4 Jan 2016

@author: ggiscan
'''
from flask import url_for

def format_user_info(users, forproduct=None):
    if forproduct is None:
        l = [(u.id, len(u.products), u.active, url_for('get_user', userid=u.id))
             for u in users]
    else:
        l = [(u.id, len(u.products), u.active, url_for('delete_product_user', prodid=forproduct, userid=u.id))
             for u in users]
    return l

def format_product_info(products, foruser=None):
    if foruser is None:
        l = [(p.id, len(p.users), url_for('get_product', prodid=p.id)) 
                for p in products]
    else:
        l = [(p.id, len(p.users), url_for('delete_user_product', userid=foruser, prodid=p.id)) 
                for p in products]
    return l