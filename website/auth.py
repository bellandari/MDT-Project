from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    
    if request.method == 'POST':
        
       username = request.form.get('username')
       password = request.form.get('password1')
       
       user = User.query.filter_by(username=username).first()
       
       if user:
           
           if check_password_hash(user.password, password):
               flash('Successful login.', category='success')
               login_user(user, remember=True)
               return redirect(url_for('views.home'))
               
           else:
               flash('Incorrect password.', category='error')
               
       else:
           flash('No matching username found.', category='error')
        
    return render_template("login.html", user=current_user)


@auth.route('/reports')
@login_required
def reports():
   return render_template("reports.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods = ['GET', 'POST'])
def register():
    
    if request.method == 'POST':
        
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(username=username).first()
        usere = User.query.filter_by(email=email).first()

        if user:
            
            flash('User already exists', category='error')
            
        elif usere:
            
            flash('Email already exists', category='error')
                    
        elif len(email) < 4:
            
            flash("Email must be greater than 4 characters", category='error')
        
        elif len(username) < 4:
            
            flash("Username must be greater than 4 characters", category='error')
        
        elif password1 != password2:
            
            flash("Passwords do not match", category='error')
        
        elif len(password1) < 7:
            
            flash("Password must be at least 7 characters", category='error')
        
        else:
            
            new_user = User(email=email, username=username, password=generate_password_hash(password2))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)

            flash('Account created!', category='success')
            
            return redirect(url_for('views.home'))
        
    return render_template("register.html", user=current_user)
