# Se importan las librerias
from random import randint
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'nutristory app'

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/login/ - this will be the login page, we need to use both GET and POST requests
@app.route('/login/', methods=['GET', 'POST'])
def login():
    #verifica si ya está logeado, en caso de estarlo hace lo devuelve a home
    if 'loggedin' in session:
        if session['id'] == "-1":
            # User is loggedin show them the home page
            return redirect(url_for('homeAdmin'))
        else:
            return redirect(url_for('home'))
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        #check admin
        if username == "admin" and password == "12345":
            session['loggedin'] = True
            session['id'] = "-1"
            session['username'] = username
            return redirect(url_for('homeAdmin'))
        else:
             # Check if account exists using MySQL
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM nutricionista WHERE usuario = %s AND pass = %s', (username, password,))
            # Fetch one record and return result
            account = cursor.fetchone()

             # If account exists in accounts table in out database
            if account:
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['idNutricionista']
                session['username'] = account['nombre']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                # Account doesnt exist or username/password incorrect
                msg = 'Usuario o Contraseña incorrectos!'

    return render_template('index.html', msg=msg)

# http://localhost:5000/login/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))


# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        if session['id'] != "-1":
            # User is loggedin show them the home page
            return render_template('home.html', username=session['username'])
        else:
            return redirect(url_for('homeAdmin'))
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/homeAdmin')
def homeAdmin():
    # Check if user is loggedin
    if 'loggedin' in session:
        if session['id'] == "-1":
            # User is loggedin show them the home page
            return render_template('homeAdmin.html', username=session['username'])
        else:
            return redirect(url_for('home'))
    # User is not loggedin redirect to login page

    return redirect(url_for('login'))


@app.route('/newNut/',methods=['GET', 'POST'])
def newNut():
    # Check if user is loggedin
    msg = ''
    if 'loggedin' in session:
        if session['id'] == "-1":
            # Check if "username" and "password" POST requests exist (user submitted form)
            if request.method == 'POST':
                # Create variables for easy access
                name = request.form['name']
                idNut = request.form['idNut']
                docType = request.form['docType']
                phone = request.form['phone']
                email = request.form['email']
                username = request.form['idNut']
                password = str(randint(10000,99999))

                # Check if account exists using MySQL
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute('INSERT INTO nutricionista (idNutricionista,nombre,usuario,pass,tipoDoc,telefono,email) VALUES (%s,%s,%s,%s,%s,%s,%s)',(idNut,name,username,password,docType,phone,email))
                mysql.connection.commit()

                return redirect(url_for('homeAdmin'))
            return render_template('newNut.html', msg=msg)
        else:
            return redirect(url_for('home'))
    # User is not loggedin redirect to login page

    return redirect(url_for('login'))

app.run()
