from datetime import datetime
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy.exc import IntegrityError
from flask_login import LoginManager, login_user, logout_user
from flask_login import UserMixin
from flask_login import login_required, current_user

basedir = os.path.abspath(os.path.dirname(__file__))
# This gives us the base directory of our project which can be used to set path 

app = Flask(__name__)
local_server = True
app.secret_key = 'super-secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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


@app.route("/")
@login_required
def home():
    curr_user_id = current_user.id
    events_lst = Event.query.filter_by(user_id=curr_user_id).all()
    print(curr_user_id)
    print(events_lst)
    event_name = []
    event_id = []
    for i in events_lst:
        event_name.append(i.ename)
    for j in events_lst:
        event_id.append(i.id)
    print(event_name)
    return render_template("home.html", uname=current_user.name.upper(), event_name=event_name, user_id=curr_user_id, event_id=event_id)


@app.route("/event", methods=['GET', 'POST'])
@login_required
def createEvent():
    if request.method == 'POST':
        event_name = request.form.get('ename')
        event_date = datetime.strptime(
            request.form.get('edate'),
            '%Y-%m-%d')
        event_date1 = f'{event_date.month}/{event_date.day}/{event_date.year}'
        # print(event_date1)
        # print('yes')
        # print(event_date, event_name)
        try:
            event = Event(user_id=current_user.id,
                          ename=event_name, edate=event_date1)
            db.session.add(event)
            db.session.commit()
            return redirect("/")
        except IntegrityError:
            return render_template("createEvent.html", message="Event Exists")
    # print('no')
    return render_template("createEvent.html")


@app.route("/timer/<user_id>/<string:event_name>",methods=['GET','POST'])
@login_required
def timer(user_id,event_name):
    events_lst = Event.query.filter_by(user_id=user_id).all()
    print(events_lst)
    for i in events_lst:
        if i.ename==event_name:
            event_date=i.edate
        print(i.id)
    return render_template("index.html",event_date=event_date)


@app.route("/login",  methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form.get('uname')
        pword = request.form.get('pword')
        user1 = User.query.filter_by(uname=uname).first()
        if not user1 or pword != user1.passwd:
            return render_template("login.html")
        login_user(user1, remember=False)
        return redirect("/")
    return render_template("login.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():
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
                return redirect("/")
            except IntegrityError:
                return render_template("signup.html", message="Username already exists")
    return render_template("signup.html")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


if __name__ == '__main__':
    app.run(debug=True)
