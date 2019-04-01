#!/usr/bin/python
import os
import sys
import logging

path = '/var/www/html/psychoSystems'

if path not in sys.path:
    sys.path.append(path)

os.environ['FLASK_CONFIG'] = 'production'
os.environ['SECRET_KEY'] = 'CHATELpsychoSystems2019!!'
os.environ['SQLALCHEMY_DATABASE_URI'] = 'mysql://psychoSystems_admin:Psycho1!@localhost/psychoSystems'

from run import app as application
