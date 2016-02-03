'''
Created on 4 Jan 2016

@author: ggiscan
'''
from core import dbman
from core.model import *
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = dbman.DB_CONNECTION
db = SQLAlchemy(app)

from . import products, users