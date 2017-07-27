from flask import Flask, request, redirect, render_template, session, flash
from mysqlconnection import MySQLConnector
app = Flask(__name__)
mysql = MySQLConnector(app,'friendsdb')
@app.route('/')
def index():
    query = "SELECT * FROM friends"                           # define your query
    friends = mysql.query_db(query)                           # run query with query_db()
    return render_template('index.html', all_friends=friends) # pass data to our template

@app.route('/friends', methods=['POST'])
def create():
    lname= request.form.get('last_name')
    fname= request.form.get('first_name')
    occup=request.form.get('occupation')

    print(mysql.query_db("INSERT INTO friends VALUES (DEFAULT,'%s','%s','%s',default,Default)"%(lname,fname,occup)))

    
    return redirect('/')
app.run(debug=True,host='0.0.0.0',port=9001)
