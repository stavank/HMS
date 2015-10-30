import os
import sys
import logging
import datetime
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../common')))
from app import app
from datab import Session
from flask import render_template, request, url_for, redirect, session
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_bcrypt import Bcrypt
from logging.handlers import RotatingFileHandler
from lib_roles.role_permissions import read_user_permissions
from models.login import Login
from models.user_roles import UserRoles


# Globals.
bcrypt = Bcrypt()
logger = logging.getLogger(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def get_mod(name):
    app.register_blueprint(
        __import__('modules.%s' % name, [], [], ['mod'], -1).mod,
        url_prefix='/%s' % name
    )

get_mod('manageusers')
get_mod('manageroles')
get_mod('managetests')
get_mod('managepatients')


# To manage the logged in user in session.
@login_manager.user_loader
def user_loader(user_id):
    q_session = Session()
    return q_session.query(Login).filter(Login.email == user_id).first()


# Displays the home page.
@app.route('/')
def login():
    session['logged_in'] = False
    if 'no-access' in session:
        msg = str(datetime.datetime.now()) + ': '+current_user.email + ' tried to access ' + session['tried']
        app.logger.info(msg)
        errormsg = 'You do not have the right to access the data you just requested ! Please login again.'
        return render_template('index.html', error=errormsg)
    else:
        return render_template('index.html')


@app.route('/loginerror')
def error_login(error):
    return render_template('index.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('has_roles', None)
    session.clear()
    logout_user()
    return redirect(url_for('.login'))


@app.route('/change-pswd', methods=['POST', 'GET'])
def change_pswd():
    if session['logged_in']:
        if request.method == 'GET':
            return render_template('changepassword.html')
        if request.method == 'POST':
            oldpswd = request.form['oldpasswd']
            newpswd = request.form['newpasswd']
            inppasswd = bcrypt.generate_password_hash(newpswd)
            q_session = Session()
            query1 = q_session.query(
                Login
            ).filter(
                Login.email == current_user.email
            ).first()
            if bcrypt.check_password_hash(query1.passwd, oldpswd):
                query2 = q_session.query(
                    Login
                ).filter(
                    Login.email == current_user.email
                ).update(
                    {
                        'passwd': inppasswd
                    }
                )
                q_session.commit()
                return redirect(url_for('.home'))
            else:
                errormsg = 'Old password does not match.'
                return render_template('changepassword.html', error=errormsg)
    else:
        return redirect(url_for('login'))


@app.route('/home')
def home():
    if session['logged_in']:
        all_permissions = read_user_permissions()
        for permission in all_permissions:
            session[permission] = True
        return render_template('home.html')
    else:
        return redirect(url_for('login'))


@app.route('/signin', methods=['POST'])
def signin():
    useremail = request.form['email']
    passwd = request.form['pwd']
    q_session = Session()
    query = q_session.query(
        Login
    ).filter(
        Login.email == useremail
    ).first()
    if query and bcrypt.check_password_hash(query.passwd, passwd):
        user = query
        user.authenticated = True
        q_session.commit()
        login_user(user, remember=True)
        msg = str(datetime.datetime.now()) + ": Successful login " + str(query.email)
        app.logger.info(msg)
        user_roles = q_session.query(
            UserRoles.user_role_id
        ).filter(
            UserRoles.email == user.email
        ).all()
        session['logged_in'] = True
        session['has_roles'] = user_roles
        return redirect(url_for('home'))
    else:
        msg = str(datetime.datetime.now()) + ": Login failure " + str(useremail)
        app.logger.info(msg)
        error = "Invalid usernme or password."
        return error_login(error)

if __name__ == '__main__':
    app.debug = True
    handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(
        host="localhost",
        port=1235
    )
