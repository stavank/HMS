from flask_login import current_user
from models.user_roles import UserRoles
from models.permissions import Permissions
from models.roles_permissions import RolesPermissions
from datab import Session


def read_user_permissions():
    q_session = Session()
    roles = q_session.query(
        UserRoles.user_role_id,
    ).filter(
        UserRoles.email == current_user.email
    ).all()
    permissions = q_session.query(
        RolesPermissions.permissions_id
    ).filter(
        RolesPermissions.role_id.in_(roles)
    ).all()
    permission_names = q_session.query(
        Permissions.name
    ).filter(
        Permissions.id.in_(permissions)
    ).all()
    user_permissions = []
    for permission_name in permission_names:
        user_permissions.append(permission_name[0])
    return user_permissions


def all_permission_names():
    q_session = Session()
    permissions = []
    query = q_session.query(
        Permissions.name
    ).all()
    for permission in query:
        permissions.append(permission[0])
    return permissions
