import datetime
from flask import Blueprint, redirect, render_template, request, url_for, session
from flask_login import current_user
from sqlalchemy import func, asc
from datab import Session
from models.roles import Roles
from models.user_roles import UserRoles
from models.permissions import Permissions
from models.roles_permissions import RolesPermissions
from lib_roles.role_permissions import all_permission_names, read_user_permissions
from app import app

mod = Blueprint('manageroles', __name__)


def read_roles():
    q_session = Session()
    query = q_session.query(
        Roles
    ).order_by(
        asc(Roles.name)
    ).all()
    result = {}
    for i in range(0, len(query)):
        result[query[i].id] = query[i].name
    return result


def read_permissions():
    q_session = Session()
    query = q_session.query(
        Permissions
    ).all()
    result = {}
    for i in range(0, len(query)):
        result[query[i].id] = query[i].name
    return result


def read_rolepermissions():
    q_session = Session()
    query = q_session.query(
        Roles.name,
        Roles.id,
        func.array_agg(RolesPermissions.permissions_id),
    ).join(
        RolesPermissions, Roles.id == RolesPermissions.role_id
    ).group_by(
        Roles.id
    ).order_by(
        asc(Roles.name)
    ).all()
    return query


@mod.route('/manage-roles')
def list_roles():
    if session['logged_in'] and ('Read roles' in session or 'Edit roles' in session):
        roles = read_roles()
        permissions = read_permissions()
        rolepermissions = read_rolepermissions()
        if roles:
            return render_template('manageroles.html', roles=roles, permissions=permissions, rolepermissions=rolepermissions)
        else:
            errormsg = "No role found. Please add a role."
            return render_template('manageroles.html', error=errormsg)
    else:
        session['no-access'] = True
        session['tried'] = 'Roles'
        return redirect(url_for('login'))


@mod.route('/create-role', methods=["POST"])
def create_role():
    if session['logged_in'] and ('Read roles' in session or 'Edit roles' in session):
        role = request.form['rolename']
        permissionslist = request.form.getlist('rolepermissions')
        q_session = Session()
        record = Roles(name=role)
        q_session.add(record)
        q_session.commit()
        query = q_session.query(
            Roles
        ).filter(
            Roles.name == role
        ).first()
        for permission in permissionslist:
            record = RolesPermissions(role_id=query.id, permissions_id=permission)
            q_session.add(record)
            q_session.commit()
        msg = str(datetime.datetime.now()) + ': Created role ' + role + ' by ' + current_user.email
        app.logger.info(msg)
        return redirect(url_for('.list_roles'))
    else:
        session['no-access'] = True
        session['tried'] = 'Roles'
        return redirect(url_for('login'))


@mod.route('/modify-role', methods=["POST"])
def modify_role():
    if session['logged_in'] and ('Read roles' in session or 'Edit roles' in session):
        if request.form['submit'] == 'delete':
            role_id = request.form['roleid']
            q_session = Session()
            # Retrieve the role name for logging
            role = q_session.query(
                Roles
            ).filter_by(
                id=role_id
            ).first()
            rolename = role.name
            # Delete the role
            roles = q_session.query(
                Roles
            ).filter_by(
                id=role_id
            ).delete()
            # delete permissions associated with the role
            permissions = q_session.query(
                RolesPermissions
            ).filter(
                RolesPermissions.role_id == role_id
            ).delete()
            # delete user role map for the said role
            user_roles = q_session.query(
                UserRoles
            ).filter(
                UserRoles.user_role_id == role_id
            ).delete()
            q_session.commit()
            msg = str(datetime.datetime.now()) + ': Deleted role ' + rolename + ' by ' + current_user.email
            app.logger.info(msg)
        if request.form['submit'] == 'save':
            role_id = request.form['roleid']
            rolename = request.form['rolename']
            q_session = Session()

            # delete all existing permissions for this role
            permissions = q_session.query(
                RolesPermissions
            ).filter(
                RolesPermissions.role_id == role_id
            ).delete()
            q_session.commit()
            permissionslist = request.form.getlist('rolepermissions')

            # get system wide permissions
            all_permissions = all_permission_names()

            # find permissions to remove from session
            permissions_to_remove_from_session = list(set(all_permissions).difference(set(read_user_permissions())))

            # remove the permissions from session
            for permission_to_remove in permissions_to_remove_from_session:
                session.pop(permission_to_remove, None)

            # set all new permissions in session
            permission_names = q_session.query(
                Permissions.name
            ).filter(
                Permissions.id.in_(permissionslist)
            ).all()

            for each_permission in permission_names:
                session[each_permission[0]] = True

            # add new role permissions
            for permission in permissionslist:
                record = RolesPermissions(role_id=role_id, permissions_id=permission)
                q_session.add(record)
                q_session.commit()
            msg = str(datetime.datetime.now()) + ': Modified role ' + rolename + ' by ' + current_user.email
            app.logger.info(msg)
        return redirect(url_for('.list_roles'))
    else:
        session['no-access'] = True
        session['tried'] = 'Roles'
        return redirect(url_for('login'))
