from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db 
from flask_login import login_user,logout_user,current_user,login_required

auth=Blueprint("auth",__name__)

@auth.route("/Signup",methods=['GET','POST'])
def sign_up():
    if request.method=="POST":
        name=request.form.get('name')
        email=request.form.get('email')
        password1=request.form.get('password1')
        password2=request.form.get('password2')

        user=User.query.filter_by(Email=email).first()

        if user:
            flash("Email already exist",category='error')
        elif len(email)<5:
            flash('Email might be more than 4 characters', category='error' )
        elif len(name)<3:
            flash('Name might be more than 3 characters', category='error' )
        elif len(password1)<5:
            flash('Password might be more than 5 characters', category='error' )
        elif (password1!=password2):
            flash('Check password', category='error' )
        else:
            user_detail=User(Name=name,Email=email,Password=generate_password_hash(password1))
            db.session.add(user_detail)
            db.session.commit()
            login_user(user_detail, remember=True)

            flash('Sign up Successfully!!', category='success')
            return redirect(url_for('views.home'))

    return render_template('signup.html',user=current_user)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(Email=email).first()
        if user:
            if check_password_hash(user.Password,password):
                login_user(user,remember=True)
                flash('Logged in Successfully !!',category='success')
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password',category='error')
        else:
            flash("Email doesn't exist", category='error')

    return render_template('login.html',user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
                               