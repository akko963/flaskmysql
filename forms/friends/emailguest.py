from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
mysql = MySQLConnector(app,'emailguestdb')
@app.route('/')
def index():
    query = "SELECT * FROM emails"                           # define your query
    guests = mysql.query_db(query)                           # run query with query_db()
    return render_template('email.html',myguests=guests) # pass data to our template
@app.route('/guests', methods=['POST'])
def create():
    email= request.form.get('email')

    print(mysql.query_db("INSERT INTO emails VALUES (DEFAULT,'%s',NOW(),NOW())"%(email)))    
    return redirect('/')
app.run(debug=True,host='0.0.0.0',port=9002)
