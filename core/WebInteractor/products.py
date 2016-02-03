'''
Created on 4 Jan 2016

@author: ggiscan
'''
from . import app, db
from flask import url_for, request, redirect
from flask.templating import render_template
from core.model import Product, User
from core import dbman
from utils import format_product_info, format_user_info

@app.route('/products/', methods=['GET'])
def get_products():
    products = db.session.query(Product).all()
    return render_template('products.html', products=format_product_info(products))


@app.route('/products/', methods=['POST'])
def new_product():
    prodid = request.form['param2']
    dbman.create_product(prodid, db.session)
    return get_products()
                                          
@app.route('/products/<prodid>', methods=['POST'])
def delete_or_put_product(prodid):
    method = request.form['param1']
    if method == 'delete':
        db.session.query(Product).filter(Product.id==prodid).delete()
        db.session.commit()
        return redirect(url_for('get_products'))
    elif method == 'put':
        product = db.session.query(Product).filter(Product.id==prodid).one()
        userid = request.form['param2']
        user = db.session.query(User).filter(User.id==userid).one()
        product.users.append(user)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('get_product', prodid=prodid))
        

@app.route('/products/<prodid>', methods=['GET'])
def get_product(prodid):
    product = db.session.query(Product).filter(Product.id==prodid).one()
    users = product.users
    other_users = [u.id for u in db.session.query(User).all() if product not in u.products]
    return render_template('users.html', 
                           product=prodid,
                           users=format_user_info(users, prodid),
                           other_users=other_users)

@app.route('/products/<prodid>/<userid>', methods=['POST'])
def delete_product_user(prodid, userid):
    product = db.session.query(Product).filter(Product.id==prodid).one()
    product.users.remove(db.session.query(User).filter(User.id==userid).one())
    db.session.commit()
    return redirect(url_for('get_product', prodid=prodid))

@app.route('/products/<prodid>/<userid>', methods=['GET'])
def get_product_user(prodid, userid):
    return redirect(url_for('get_user', userid=userid))
