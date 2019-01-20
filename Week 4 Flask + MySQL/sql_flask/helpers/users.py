from flask import Flask, render_template, redirect, session, request, flash
from mysqlconnection import MySQLConnector
import re
from datetime import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)

def validate(form_data):
    errors = []
    if len(form_data['first_name']) < 2:
        errors.append('First name must be at least 2 characters long')

    if len(form_data['last_name']) < 2:
        errors.append('Last name must be at least 2 characters long')

    if len(form_data['password']) < 8:
        errors.append('Password must be at least 8 characters long')

    if form_data['password'] != form_data['confirm']:
        errors.append('Passwords do not match')

    if not EMAIL_REGEX.match(form_data['email']):
        errors.append("Email must be valid")
    
    return errors

def create(form_data, bcrypt):
    # pw_hash = bcrypt.generate_password_hash(form_data['password'])
    pw_hash = "jdsofdnewofin"
    db = MySQLConnector(app, 'mydb_janurary')

    data = {
    'first_name': request.form['first_name'],
    'last_name': request.form['last_name'],
    'email': request.form['email'],
    'pw_hash': pw_hash,
    'updated_at': datetime.now()
    }

    columns = ', '.join("`" + str(x).replace('/', '_') + "`" for x in data.keys())
    values = ', '.join("'" + str(x).replace('/', '_') + "'" for x in data.values())
    query = "INSERT INTO %s (%s) VALUES (%s);" % ("USERS", columns, values)
    user_id = db.query_db(query, data)
    return user_id

def login(form_data, bcrypt):
    db = MySQLConnector(app, 'mydb_janurary')

    data = {
        "email": request.form["email"]
    }
    query = "SELECT email, pw_hash, id FROM users WHERE email = 'bjbibijbi@hotmail.com';"

    print ("88888888888888")
    print (db.query_db(query, data))