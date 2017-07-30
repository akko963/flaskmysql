from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]+$')

app = Flask(__name__)
app.secret_key = 'nobodyknows'
mysql = MySQLConnector(app,'fullfriendsdb')

@app.route('/')
def index():
    query = "SELECT * FROM friends"                           # define your query
    myfriends = mysql.query_db(query)      
    for friend in myfriends:
       friend['actionline']='<form action="/friends/%s/delete" method="POST"><input type="submit" value="Delete"></form><form action="/friends/%s/edit" method="GET"><input type="submit" value="Edit"></form>'%(friend["id"],friend["id"])
    return render_template('fullfriends.html',myfriends=myfriends) # pass data to our template

@app.route('/friends', methods=['POST'])
def create():
    fname= request.form.get('first_name')
    lname= request.form.get('last_name')
    email= request.form.get('email')
    if EMAIL_REGEX.match(request.form.get('email')) :
      flash("The info [ %s %s %s ] you've entered is valid."%(email,fname,lname))
      print(mysql.query_db("INSERT INTO friends VALUES (DEFAULT,'%s','%s','%s',NOW(),NOW())"%(fname,lname,email))) 
    else:
      flash("Invalid Entry.")
    return redirect('/')

@app.route('/friends/<id>/edit', methods=['GET'])
def edit(id):
    friends = mysql.query_db("SELECT * FROM friends WHERE friends.id=%s"% id   )
    if not friends:
      flash("User id does not exist.")
    return render_template('fullfriends-edit.html',editid=id,toedit=friends[0])

@app.route('/friends/<id>', methods=['POST'])
def update(id):
    friends = mysql.query_db("SELECT * FROM friends WHERE friends.id=%s"% id   )
    if not friends:
      flash("User id does not exist.")
    else: 
       fname= request.form.get('first_name')
       lname= request.form.get('last_name')
       email= request.form.get('email')      
       mysql.query_db("UPDATE friends SET first_name='%s', last_name='%s', email='%s' where friends.id=%s"%(email,fname,lname,id))
       flash("Updated Record %s with %s, %s, %s"%(id,fname,lname,email))
    return redirect('/')

@app.route('/friends/<id>/delete', methods=['POST'])
def destroy(id):
    if mysql.query_db("SELECT * FROM friends WHERE friends.id=%s"% id   )   :
      mysql.query_db("DELETE FROM friends WHERE friends.id=%s"%id)
      flash("Record %s deleted from our database"%id)
    else:
      flash("Record %s does not exist"%id)
    return redirect('/')

app.run(debug=True,host='0.0.0.0',port=9003)
