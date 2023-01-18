from flask import Blueprint, render_template, session, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user
from .models import User
from . import db
import re
import flask_bcrypt
from .mail import Mail

auth = Blueprint('auth',__name__)

@auth.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user:
            if flask_bcrypt.check_password_hash(user.password,password):
                login_user(user)
                return redirect(url_for('views.dashboard'))
            else:
                flash("Incorrect Password!")
        else:
            flash("User does not exist")
    return render_template('login.html')

@auth.route('/forgot_password',methods=['GET','POST'])
def forgot_pw():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            password = user.password
            subject = "Password Recovery for Event Management app"
            body = "Dear"+user.name+"\nYour password is "+password+"\n\nThanks and Regards\nEvent Management Apps"
            Mail(email,subject,body)
        else:
            flash("Email Does not exist!")
    return render_template('password.html')

@auth.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        cpassword = request.form['cpassword']

        existing_user = User.query.filter_by(email=email).first()
        if not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash("Invalid Email Address")
            return redirect(url_for('auth.signup'))
        elif existing_user:
            flash("Email Already Existed, Please choose another one.")
            return redirect(url_for('auth.signup'))
        elif password != cpassword:
            flash("Password does not match!")
            return redirect(url_for('auth.signup'))
        else:
            encrypt_password = flask_bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(name=fname+" "+lname, email=email, phone=phone, password=encrypt_password)
            db.session.add(user)
            db.session.commit()
            flash("You have successfully Registered")
            subject="Successfull Registration"
            body= "Dear"+fname+" "+lname+",\n\n You've successfully signed up into our application.\n The loging information are as follows:\n"+"email: "+email+"\n"+"password: "+password+"\n\n\nThanks and Regards\n Event Manage App"

            #Function to send mail
            #Mail(email,subject,body)
            return redirect(url_for('auth.login'))
    return render_template('signup.html')



