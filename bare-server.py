from flask import Flask,jsonify
import json
# import the Connector function
from mysqlconnection import MySQLConnector
app = Flask(__name__)
# connect and store the connection in "mysql" note that you pass the database name to the function
mysql = MySQLConnector(app, 'fullfriendsdb')
# an example of running a query
print(mysql.query_db("SELECT * FROM friends"))

@app.route('/')
def index():
   answers= mysql.query_db("SELECT * FROM friends WHERE friends.id=10") 
   print(answers)
   if answers== None:
      print("none")
   elif answers==[]:
      print("empty list")
   else:
      print("maybe empty list")
   #print(jsonify(answers))
   return "hi"

app.run(debug=True,port=9000,host='0.0.0.0')

