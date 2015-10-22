from app.extensions import db
from datetime import datetime
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .sqlalchemy_helpers import CaseInsensitiveWord
from sqlalchemy.ext.hybrid import hybrid_property


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(255), unique=True)

    oauthId = db.Column(db.String(50))
    oauthProvider = db.Column(db.String(50))

    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))

    pwdhash = db.Column(db.String(255))

    avatarPath = db.Column(db.String(255), default='avatar.jpg')
    dateJoined = db.Column(db.DateTime(), default=datetime.utcnow)

    isAdmin = db.Column(db.Boolean(), default=False)

    articles = db.relationship('Articles', backref='author', lazy='dynamic')
    comments = db.relationship('Comments', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        password = kwargs.pop('password')
        self.set_password(password)
        super(Users, self).__init__(**kwargs)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)

    @property
    def url(self):
        return url_for('users.get_user_by_id', id=self.id, _external=True)

    @hybrid_property
    def fullname(self):
        fullname = ''
        if isinstance(self.firstName, basestring):
            fullname = self.firstName
        if isinstance(self.lastName, basestring):
            fullname += ' ' + self.lastName
        return fullname

    @hybrid_property
    def username_insensitive(self):
        return self.username.lower()

    @username_insensitive.comparator
    def username_insensitive(self):
        return CaseInsensitiveWord(self.username)

    @hybrid_property
    def email_insensitive(self):
        return self.email.lower()

    @email_insensitive.comparator
    def email_insensitive(self):
        return CaseInsensitiveWord(self.email)

    def is_admin(self):
        return self.isAdmin
