from flask import Flask, request, redirect, render_template, session, flash
from flask_bcrypt import Bcrypt
from mysqlconnection import MySQLConnector
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]+$')
USER_REGEX = re.compile(r'^[a-zA-Z]{1}[a-zA-z\._-]{3,20}$')
NAME_REGEX = re.compile(r'^[a-zA-Z]{2}[a-zA-z ]*$')
PASS_REGEX = re.compile(r'^[a-zA-Z@#$%_-]{8,21}$')
msgs = "SELECT messages.id,messages.user_id,messages.message,messages.created_at,user.user_name,user.first_name,user.last_name from messages join user on user.id = messages.user_id ORDER BY messages.created_at DESC"

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'nobodyknows'
mysqlwall = MySQLConnector(app,'walldb')

@app.route('/')  # Route shows a login form (div) if no #session else user info
  # check session. (if session exists retrieve self's info)
def index():

   if not 'uid' in session:
      return render_template('wall-login.html')
   pendingnodes=[]
   msgs = mysqlwall.query_db("SELECT messages.id,messages.user_id,messages.message,messages.created_at,user.user_name,user.first_name,user.last_name from messages join user on user.id = messages.user_id ORDER BY messages.created_at DESC")
   for msg in msgs:
      code = "<h5 class='msghead'>%s - %s</h5>"%(msg['user_name'],msg['created_at'].strftime('%Y-%m-%d %I:%M %p'))+\
      "<a class='dellink' href='/delete/msg/%s'>Delete</a>" %msg['id']+\
      "<div class='msgbox'><p class='message'>%s</p></div>"%msg['message']
      

      pendingnodes.append(code)
      comments = mysqlwall.query_db("SELECT comments.id,comments.user_id,comments.message_id,comments.comment,comments.created_at,user.user_name,user.first_name,user.last_name from comments join user on user.id = comments.user_id  where comments.message_id=%s ORDER BY comments.created_at DESC"%msg['id']) 

      for cmt in comments:
         code = "<h5 class='cmthead'>%s - %s</h5>"%(cmt['user_name'],cmt['created_at'].strftime('%Y-%m-%d %I:%M %p'))+\
        "<a class='dellink' href='/delete/cmt/%s'>Delete</a>" %cmt['id']+\
         "<div class='cmtbox'><p class='message'>%s</p></div>"%cmt['comment']
         
         pendingnodes.append(code)
      

      code = '<form class="cmtform" action="/post" method="POST"><textarea name="cmtpost" rows =4 cols=100 value=""></textarea><input type="hidden" name="msgid" value="%s"><input class="cmtbutton" type="submit" value="Comment"></form>' %msg['id']
      pendingnodes.append(code)
# 'class="comment"',user,created_at

   return render_template('wall.html',msgs=pendingnodes)



#it will keep coming back here if registration fails
@app.route('/register')
def register():    
   return render_template('wallreg.html')

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
      flash(error,'error')
      return redirect('/register')
   pwd = bcrypt.generate_password_hash(pwd).decode('utf8')
   uid = mysqlwall.query_db("INSERT INTO user VALUES (DEFAULT,'%s','%s','%s','%s','%s',NOW(),NOW())"%(user,fname,lname,email,pwd))
   if uid:
      session['uid']= uid
      session['user_name']= user
      session['first_name']=fname
      session['last_name']=lname
      session['email']=email
      flash("Success! "+user+" is registered into Registration Demo.",'success')
   return redirect('/')

# will pull a query from db and check the savedhash against the entry
# initiate session
@app.route('/login',methods =['POST']) #receive info from login-form(/)
def login():  # check db, let him log-in by init'ing session
   user = request.form.get('user_name')
   pwd  = request.form.get('password')
   records = mysqlwall.query_db ("SELECT id,user_name,first_name,last_name,email,password FROM user where user.user_name ='%s'"%user)
   if not records:
      flash("User does not exist!",'error')
      return redirect('/')

   # IT is a single record
   savedhash = records[0].get('password')
   print("\n\nUser found. hash retrieved %s against %s\n\n"%(savedhash,pwd ))
   if bcrypt.check_password_hash(savedhash,pwd) :
      session['user_name']= user
      session['uid'] = records[0].get('id')
      session['first_name']=records[0].get('first_name')
      session['last_name']=records[0].get('last_name')
      session['email']=records[0].get('email')
   else: 
      flash("Passwords do not match!",'error')
   return redirect('/')

# call the cleanup (clear the session)
@app.route('/logout')
def logout():
   if 'user' in session:
      session.pop('user')
   if 'uid' in session:
      session.pop('uid')
   if 'first_name' in session:
      session.pop('first_name')
   if 'last_name' in session:
      session.pop('last_name')
   if 'email' in session:
      session.pop('email')
   flash("Successfully logged out.",'success')
   return redirect('/')
@app.route('/post',methods=['POST'])
def post():
   print(request.form.get('msgpost'),request.form.get('cmtpost'))
   if not 'uid' in session:
      return redirect('/')
   elif  request.form.get('msgpost'):
      if mysqlwall.query_db("INSERT INTO messages (id,user_id,message,created_at,updated_at) VALUES (DEFAULT,%d,'%s',NOW(),NOW() )"  %(session['uid'],request.form.get('msgpost')) ):
         flash('Message posted successfully!','success')
   elif request.form.get('cmtpost'):
      if mysqlwall.query_db("INSERT INTO comments (id,message_id,user_id,comment,created_at,updated_at) VALUES (DEFAULT,%s,%d,'%s',NOW(),NOW() )"  %(request.form.get('msgid'),session['uid'],request.form.get('cmtpost')) ):
         flash('Comment posted successfully!','success')

   return redirect('/')

@app.route('/delete/<type>/<id>',methods=['GET'])
def delete(type,id):
   print('delete test',type,id)
   if not 'uid' in session:
      flash('Session timed out!','warning')
      return redirect('/')
   elif  type=='msg':
      if mysqlwall.query_db("SELECT * FROM comments where comments.message_id = %s"% id):
         flash('Message cannot be deleted with existing comments','error')
      elif not timecheck( mysqlwall.query_db("SELECT created_at FROM messages where id = %s"% id)):
         flash('Message cannot be deleted after 30mins','error')
      elif mysqlwall.query_db("DELETE FROM messages Where id=%s"  %id) :
         flash('Message deleted successfully!','success')
   elif type=='cmt':
      if not timecheck( mysqlwall.query_db("SELECT created_at FROM comments where id=%s"%id)):
         flash('Message cannot be deleted after 30mins','error')
      elif mysqlwall.query_db("DELETE FROM comments Where id=%s"  %id) :
         flash('Comment deleted successfully!','success')
   else:
      flash('Unknown error. Insufficient data provided for deletion.','error')
   return redirect('/')

def timecheck(msgtimeData):
   import datetime
   print("#########################################",msgtimeData)
   msgtimeData = msgtimeData[0]
   msgtime = msgtimeData['created_at']
   timedelta =  datetime.datetime.now() - msgtime 
   print(timedelta,timedelta.total_seconds())
   return timedelta.total_seconds() < 30*60 #( less than 30mins = true)


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


# Features to add; to consider: Make the  registration page refilled after rejected reg.
# Highlight the error-fields. Display all the error messages. Preferably next to their respective input field.