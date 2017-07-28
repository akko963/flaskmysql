from flask import Flask, request, redirect, render_template, session, flash
from flask_bcrypt import Bcrypt
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]+$')
USER_REGEX = re.compile(r'^[a-zA-Z]{1}[a-zA-z\._-]{3,20}$')
NAME_REGEX = re.compile(r'^[a-zA-Z]{2}[a-zA-z ]*$')
PASS_REGEX = re.compile(r'^[a-zA-Z@#$%_-]{8,21}$')
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'nobodyknows'
mysql = MySQLConnector(app,'reguserdb')

@app.route('/')  # Route shows a login form (div) if no #session else user info
  # check session. (if session exists retrieve self's info)
def index():
   print("re routed to main",session.get('validated'))
   if 'validated' in session:
      return render_template('myinfo.html')
   else:
      return render_template('login.html')

#it will keep coming back here if registration fails
@app.route('/register')
def register():    
   return render_template('register.html')

# trigger the registration process, check for valid inputs and enter into db
# at success redirected to root /; where it is again sent back to info page.
# at fail: send it back to /register
@app.route('/register/new',methods=['POST'])
def registernew():
   user,fname,lname,email,pwd=request.form.get('user_name'),request.form.get('first_name'),\
            request.form.get('last_name'),request.form.get('email'),request.form.get('password')

   error = checkErrors(user,fname,lname,email,pwd) 
   if not error: # if no error found from prev checks
      error = None if pwd == request.form.get('confirm')  else "Passwords do not match"
   if error != None : # error
      flash(error)
      return redirect('/register')
   pwd = bcrypt.generate_password_hash(pwd).decode('utf8')

   if mysql.query_db("INSERT INTO users VALUES (DEFAULT,'%s','%s','%s','%s','%s',NOW(),NOW())"%(user,fname,lname,email,pwd)):
      session['validated']= True
      session['user_name']= user
      session['first_name']=fname
      session['last_name']=lname
      session['email']=email
      flash("Success! "+user+" is registered into Registration Demo.")
   return redirect('/')

# will pull a query from db and check the savedhash against the entry
# initiate session
@app.route('/login',methods =['POST']) #receive info from login-form(/)
def login():  # check db, let him log-in by init'ing session
   user = request.form.get('user_name')
   pwd  = request.form.get('password')
   records = mysql.query_db ("SELECT user_name,first_name,last_name,email,password FROM users where users.user_name ='%s'"%user)
   if not records:
      flash("No such user")
      return redirect('/')

   # IT is a single record
   savedhash = records[0].get('password')
   print("\n\nUser found. hash retrieved %s against %s\n\n"%(savedhash,pwd ))
   if bcrypt.check_password_hash(savedhash,pwd) :
      session['validated']= True
      session['user_name']= user
      session['first_name']=records[0].get('first_name')
      session['last_name']=records[0].get('last_name')
      session['email']=records[0].get('email')
   else: 
      flash("Password did not match")
   return redirect('/')

# call the cleanup (clear the session)
@app.route('/logout')
def logout():
   if 'validated' in session:
      session.pop('validated')
   if 'user' in session:
      session.pop('user')
   if 'first_name' in session:
      session.pop('first_name')
   if 'last_name' in session:
      session.pop('last_name')
   if 'email' in session:
      session.pop('email')
   return redirect('/')

@app.route('/allusers',methods=['GET'])
   # retrieve user names
def allusers():
   ans = mysql.query_db("SELECT * from users")
   return render_template('allusers.html',records = ans)

#check errors on users, their names and passwords
def checkErrors(user,fname,lname,email,pwd):
   if not USER_REGEX.match(user):
      return "User name must have 4-21 characters (alphabets and digits)"
   if not NAME_REGEX.match(fname):
      return "First name must have at least 2 alphabets."
   if not NAME_REGEX.match(lname):
      return "Last name must have at least 2 alphabets."

   if not EMAIL_REGEX.match(email):
      return "Please enter a valid Email."
   if not PASS_REGEX.match(pwd):
      return "Password must have 8-21 characters (alphabets, digits and some special characters)"
   return None

app.run(debug=True,host='0.0.0.0',port=9004)
