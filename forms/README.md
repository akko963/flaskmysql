## email-guest book

`emailguest.py`

`mysqlconnection.py`  

`templates/email.html`

## friends

`server.py`

`templates/index.html`

`mysqlconnection.py`

## full friends app

`templates/fullfriends.html`  # **index page**

`templates/fullfriends-edit.html` # **edit page**

`fullfriends.py`  # ** server code and application **

`mysqlconnection.py` #  **mysqlconnection stuff**

## register app

`reguser.py`    # **server code and application**

`templates/register.html`  **template**

`mysqlconnection.py`  **Mysql code _unchanged_**

`reguserdb-walldb-create.sql` **database file**

## reguserdb-walldb-create.sql

## The Dojo Wall app

`thewall.py`    # **server code and application**

`templates/wall.html`  **main template**

`templates/wallreg.html`  **template for register form**

`templates/wall-login.html`  **template for login form**

`mysqlconnection.py`  **Mysql code _unchanged_**

`reguserdb-walldb-create.sql` **database file**

## User DB app

`userdb.py`    # **server code and application**

`templates/getall.html`  **main template, get all users**

`templates/adduser.html`  **template for add form**

`templates/getuser.html`  **template for get one user**

`templates/edituser.html`  **template for edit form**

`mysqlconnection.py`  **Mysql code _unchanged_**

`userdb.sql` **database file schema. no template**



#### notes
```
current sql operations in this dir: insert/delete/select simple commands
CRUD in the full friends app
Register app - *Semi-RESTful*
THE WALL app - No Update from CRUD
userdb : full CRUD semi-RESTFUL
```
