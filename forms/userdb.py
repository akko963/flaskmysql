from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
import re

app = Flask(__name__)
app.secret_key = 'nobodyknows'
mysql = MySQLConnector(app,'userdb')

# USING DB : usersdb
# table users
# columns: id, name, email, created_at,updated_at
# queries
# select all columns all rows
getallquery = "SELECT * FROM users"
# select all columns, one row match, LIMIT 1
getquery = "SELECT * FROM users where id = %s"  #id is primary/autoinc
# add one row
addquery = "INSERT INTO users values(DEFAULT,'%s','%s','%s',DEFAULT,DEFAULT)"
# edit one row
updatequery = "UPDATE users SET first_name='%s', last_name='%s', email='%s' where id=%s"
# delete one row match
delquery = "DELETE FROM users where id = %s"

# /users  : get, show all users page
@app.route('/users')
def index():#@todo   
    myusers = mysql.query_db(getallquery)      
    #for user in myusers:
       #pass
    return render_template('getall.html',myusers=myusers) # pass data to our template

# /users/<id>   : get, user's individual info page
@app.route('/users/<id>')
def getuser(id):
    myusers = mysql.query_db(getquery%id)
    #for user in myusers:
        #pass     
    return render_template('getuser.html',user=myusers[0]) # pass data to our template

# /users/new  : get , add-user page
@app.route('/users/new')
def addform():
    # no query / only display form
    #for user in myusers:
       #user['actionline']='<form action="/friends/%s/delete" method="POST"><input type="submit" value="Delete"></form><form action="/friends/%s/edit" method="GET"><input type="submit" value="Edit"></form>'%(myusers["id"],friend["id"])
    return render_template('adduser.html') # pass data to our template

# ->> /users/create  : post,handle "POST" from add-user page
@app.route('/users/create',methods=['POST'])
def postadd():
    id = mysql.query_db(addquery%\
      (request.form['fname'],request.form['lname'],request.form['email']))
    return redirect('/users/%s'%id)

# /users/<id>/edit  : get, gives user edit form
@app.route('/users/<id>/edit',methods=['GET'])
def editform(id):
    myusers = mysql.query_db(getquery%id)
    return render_template('edituser.html',user=myusers[0]) # pass data to our template

# /users/<id>/edit  : post handle POST from edit page
@app.route('/users/<id>/edit',methods=['POST'])
def postedit(id):
    myusers = mysql.query_db(updatequery%(request.form['fname'],request.form['lname'],request.form['email'],id))
    return redirect('/users/%s'%id)

# /sers/<id>/destroy : get,apply user deletion
@app.route('/users/<id>/destroy')
def deluser(id):
    myusers = mysql.query_db(delquery%id)
    return redirect('/users')

# Templates: 1. all 2. each 3. add 4. edit
# POST: 1. create 2. edit 3. destroy



# Find out which dynamic content needs to be generated as HTML
# prepare the strings sending back to frontend
# Here in userdb app 
# '/' route, index() : Each rows of users should be prepared 
# adding with show/edit/delete links


app.run(debug=True,host='0.0.0.0',port=9005)
