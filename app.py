from datetime import datetime
from email import message
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_user, logout_user
from flask_login import UserMixin
from flask_login import login_required, current_user
# flask-login library is used to check user authentication
# like django-allauth

basedir = os.path.abspath(os.path.dirname(__file__))
# This gives us the base directory of our project which can be used to set path

app = Flask(__name__)
local_server = True
app.secret_key = 'super-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# We include sqlite database using these lines of code

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
# These are settings for flask-login
# login-view is our login page


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# Component required for flask-login
# Write same code as it is fro User Login
# loads the user


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    uname = db.Column(db.String(80), unique=True, nullable=False)
    passwd = db.Column(db.String(80), nullable=False)


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    ename = db.Column(db.String(100), nullable=False)
    edate = db.Column(db.String(100), nullable=False)

# After importing sqlite database.db file using sqlalchemy we create our models
# after creating models do:
    # in terminal write
    # python
    # from app import db
    # db.drop_all()
    # db.create_all()

# This creates the tables referencing to the Models created in database.db file

@app.route("/")
@login_required
# using flask-login we can use login_required
# page will only open if user is logged in
def home():
    print(current_user.is_authenticated)
    curr_user_id = current_user.id
    # current_user gives us the info about the current user that is logged in
    events_lst = Event.query.filter_by(user_id=curr_user_id).all()
    event_name = []
    event_id = []
    for i in events_lst:
        event_name.append(i.ename)
    for j in events_lst:
        event_id.append(i.id)
    return render_template("home.html", uname=current_user.name.upper(), event_name=event_name, user_id=curr_user_id, event_id=event_id)


@app.route("/event", methods=['GET', 'POST'])
@login_required
def createEvent():
    if request.method == 'POST':
        event_name = request.form.get('ename')
        event_date = datetime.strptime(
            request.form.get('edate'),
            '%Y-%m-%d')
        # strptime function of datetime strips the time data into individual components
        event_date1 = f'{event_date.month}/{event_date.day}/{event_date.year}'
        try:
            event = Event(user_id=current_user.id,
                          ename=event_name, edate=event_date1)
            db.session.add(event)
            db.session.commit()
            return redirect("/")
        except IntegrityError:
            return render_template("createEvent.html", message="Event Exists")
    return render_template("createEvent.html")


@app.route("/timer/<user_id>/<string:event_name>", methods=['GET', 'POST'])
# Giving parameters to flask route
@login_required
def timer(user_id, event_name):
    events_lst = Event.query.filter_by(user_id=user_id).all()
    print(events_lst)
    for i in events_lst:
        if i.ename == event_name:
            event_date = i.edate
            e_date = datetime.strptime(
                event_date,
                '%m/%d/%Y')
            print(e_date)
            event_date1=f'{e_date.strftime("%B")} {e_date.day}, {e_date.year}'
            print(event_date1)
            event_name = i.ename
            break
        print(i.id)
    return render_template("index.html", event_date=event_date, event_name=event_name.upper(),event_date_words=event_date1)


@app.route("/login",  methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST' and 'uname' in request.form and 'pword' in request.form:
            uname = request.form.get('uname')
            pword = request.form.get('pword')
            user1 = User.query.filter_by(uname=uname).first()
            if not user1 or pword != user1.passwd:
                return render_template("login.html",message="Username or Password Incorrect!!")
            login_user(user1, remember=False)
            # This sets the logged in user as the current user using flask-login
            return redirect("/")
    return render_template("login.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect("/")
    else:
        if request.method == 'POST' and 'uname' in request.form and 'pword' in request.form:
            name = request.form.get('name')
            uname = request.form.get('uname')
            passwd = request.form.get('pword')
            passwd2 = request.form.get('pword2')

            if passwd == passwd2:
                try:
                    user = User(name=name, uname=uname, passwd=passwd)
                    db.session.add(user)
                    db.session.commit()
                    user1 = User.query.filter_by(uname=uname).first()
                    if not user1 or passwd != user1.passwd:
                        return render_template("login.html")
                    login_user(user1, remember=False)
                    return redirect("/")
                except IntegrityError:
                    return render_template("signup.html", message="Username already exists")
    return render_template("signup.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")
# logout view using flask-login


if __name__ == '__main__':
    app.run(debug=True)

# generate requirements.txt file using this command
# python3 -m  pipreqs.pipreqs .
