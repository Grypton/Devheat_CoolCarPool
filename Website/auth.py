from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint("auth",__name__)


@auth.route("/login", methods = ['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('Logged in successfully')
            else:
                flash('Incorrect password, try again.',category='error')
        else:
            flash('Email does not exist',category='error')

    return render_template("login.html", boolean = True)

@auth.route("/signup", methods = ['GET','POST'])
def signup():          
    return render_template("signup.html")

@auth.route("/signup-rider", methods = ['GET','POST'])
def signup_rider():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm-password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email must be greater than 3 characters.', category='error')
        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password != confirm_password:
            flash('Passwords don\'t match.', category='error')
        elif len(password) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else: 
            new_user =User(email= email,username=username,password=generate_password_hash(password,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Account Created', category = 'success')
            return redirect(url_for('views.home'))
    return render_template("signup_rider.html")


@auth.route("/signup-driver", methods = ['GET','POST'])
def signup_driver():
    return render_template("signup_driver.html")


@auth.route("/search", methods = ['GET','POST'])
def search():
    return render_template("search.html")