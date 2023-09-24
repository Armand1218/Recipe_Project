from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import Person
from flask_app.models import recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():

    if not Person.user_validate_registration(request.form):
        return redirect('/')
    data={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
        }
    id = Person.save_db(data)
    session['user_id'] = id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def login():
    user = Person.user_get_email(request.form)
    if not user: 
        flash('Wrong Email or Password', "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Wrong Password', "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("car_dashboard.html", user = Person.user_get_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')