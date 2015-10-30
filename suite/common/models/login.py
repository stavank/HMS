from sqlalchemy import Column, String, Boolean
from datab import BaseForModels


class Login (BaseForModels):
    __tablename__ = 'login'

    email = Column(String, primary_key=True)
    passwd = Column(String)
    authenticated = Column(Boolean)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def __init__(self, email, passwd, authenticated):
        self.email = email
        self.passwd = passwd
        self.authenticated = authenticated
