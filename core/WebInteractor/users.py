'''
Created on 4 Jan 2016

@author: ggiscan
'''
from . import app, db
from flask import url_for, request, redirect
from flask.templating import render_template
from core.model import User, Product
from core import dbman
from utils import format_product_info, format_user_info

@app.route('/users/', methods=['GET'])
def get_users():
    users= db.session.query(User).all()
    return render_template('users.html', users=format_user_info(users))

@app.route('/users/', methods=['POST'])
def new_user():
    userid = request.form['param2']
    user = User(id=userid, password="")
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('get_users'))

@app.route('/users/<userid>', methods=['GET'])
def get_user(userid):
    user = db.session.query(User).filter(User.id==userid).one()
    products = user.products
    other_products = [p.id for p in db.session.query(Product).all() if user not in p.users ]
    return render_template('user.html', 
                           user=(user.id, user.active, user.creation_date), 
                           products=format_product_info(products, user.id),
                           other_products=other_products)

@app.route('/users/<userid>', methods=['POST'])
def delete_or_put_user(userid):
    method = request.form['param1']
    if method == 'delete':
        db.session.query(User).filter(User.id==userid).delete()
        db.session.commit()
        return redirect(url_for('get_users'))
    elif method == 'put':
        prodid = request.form['param2']
        dbman.register_user(prodid, userid, None, db.session)
        return redirect(url_for('get_user', userid=userid))
    elif method == 'put_active':
        active = request.form['param2']
        active = True if active == 'true' else False 
        user = db.session.query(User).filter(User.id==userid).one()
        user.active = active
        db.session.commit() 
        return redirect(url_for('get_user', userid=userid))
    
@app.route('/users/<userid>/<prodid>', methods=['POST', 'DELETE'])
def delete_user_product(userid, prodid):
    user = db.session.query(User).filter(User.id==userid).one()
    product = db.session.query(Product).filter(Product.id==prodid).one()
    user.products.remove(product)
    db.session.commit()
    return redirect(url_for('get_user', userid=userid))

@app.route('/users/<userid>/<prodid>', methods=['GET'])
def get_user_product(userid, prodid):
    return redirect(url_for('get_product', prodid=prodid))
