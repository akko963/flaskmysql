from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = 'nobodyknows'
mysql = MySQLConnector(app,'emailguestdb')
@app.route('/')
def index():
    query = "SELECT * FROM emails"                           # define your query
    guests = mysql.query_db(query)      
    for email in guests:
       email['deleteline']='<form action="/guests" method="POST"><input type="hidden" value=%d name="id"><input type="submit" name="action" value="Delete"></form>'%email["id"]
       print(email['deleteline'])
    return render_template('email.html',myguests=guests) # pass data to our template
@app.route('/guests', methods=['POST'])
def modify():
    if request.form.get('action') == 'Add':
       email= request.form.get('email')
       if EMAIL_REGEX.match(request.form.get('email')) :
         flash("The email [ %s ] you've entered is valid."%(email))
         print(mysql.query_db("INSERT INTO emails VALUES (DEFAULT,'%s',NOW(),NOW())"%(email)))    
       else:
         flash("Invalid email.")
    else:
      mysql.query_db("DELETE FROM emails WHERE emails.id=%d"%int(request.form.get('id')))
      flash("Record %s is deleted from emailguest database"%request.form.get('id'))
    return redirect('/')
app.run(debug=True,host='0.0.0.0',port=9002)
