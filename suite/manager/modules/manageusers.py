import datetime
from flask import Blueprint, redirect, render_template, request, url_for, session
from flask_login import current_user
from flask_bcrypt import Bcrypt
from sqlalchemy import func, asc
from datab import Session
from models.roles import Roles
from models.login import Login
from models.user_roles import UserRoles
from app import app

mod = Blueprint('manageusers', __name__)

bcrypt = Bcrypt()


def read_roles():
    q_session = Session()
    query = q_session.query(
        Roles
    ).all()
    result = {}
    for i in range(0, len(query)):
        result[query[i].id] = query[i].name
    return result


@mod.route('/manage-users')
def user_roles():
    if session['logged_in'] and ('Read users' in session or 'Edit users' in session):
        roles = read_roles()
        q_session = Session()
        query = q_session.query(
            UserRoles.email,
            func.array_agg(UserRoles.user_role_id)
        ).group_by(
            UserRoles.email
        ).order_by(
            asc(UserRoles.email)
        ).all()
        if query:
            return render_template('manageusers.html', roles=roles, usersandroles=query)
        else:
            errormsg = "No roles found. Please add roles and assign them to users."
            return render_template('manageusers.html', error=errormsg)
    else:
        session['no-access'] = True
        session['tried'] = 'Users'
        return redirect(url_for('login'))


@mod.route('/create-user', methods=['POST'])
def create_user():
    if session['logged_in'] and ('Read users' in session or 'Edit users' in session):
        roleslist = request.form.getlist('newuserroles')
        user = request.form['username']
        passwd = request.form['passwd']
        inppasswd = bcrypt.generate_password_hash(passwd)
        q_session = Session()
        userrecord = Login(email=user, passwd=inppasswd, authenticated=True)
        q_session.add(userrecord)
        q_session.commit()
        for role in roleslist:
            record = UserRoles(email=user, user_role_id=role)
            q_session.add(record)
            q_session.commit()
        msg = str(datetime.datetime.now()) + ': Created user with id = ' + user + ' by ' + current_user.email
        app.logger.info(msg)
        return redirect(url_for('.user_roles'))
    else:
        session['no-access'] = True
        session['tried'] = 'Users'
        return redirect(url_for('login'))


@mod.route('/modify-users', methods=['POST'])
def modify_users():
    if session['logged_in'] and ('Read users' in session or 'Edit users' in session):
        if request.form['submit'] == 'save':
            roleslist = request.form.getlist('roleslist')
            username = request.form['usernameholder']
            q_session = Session()
            roles = q_session.query(
                UserRoles
            ).filter_by(
                email=username
            ).delete()
            q_session.commit()
            for role in roleslist:
                record = UserRoles(email=username, user_role_id=role)
                q_session.add(record)
                q_session.commit()
            msg = str(datetime.datetime.now()) + ': Made changes to roles of ' + username + ' by ' + current_user.email
            app.logger.info(msg)

        if request.form['submit'] == 'delete':
            user = request.form['usernameholder']
            q_session = Session()
            roles = q_session.query(
                UserRoles
            ).filter_by(
                email=user
            ).delete()
            q_session.commit()
            users = q_session.query(
                Login
            ).filter_by(
                email=user
            ).delete()
            q_session.commit()
            msg = str(datetime.datetime.now()) + ': Removed user ' + user + ' by ' + current_user.email
            app.logger.info(msg)

        return redirect(url_for('.user_roles'))
    else:
        session['no-access'] = True
        session['tried'] = 'Users'
        return redirect(url_for('login'))
