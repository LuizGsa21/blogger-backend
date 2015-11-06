import pprint
from app.extensions import db
from datetime import datetime
from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .sqlalchemy_helpers import CaseInsensitiveWord
from sqlalchemy.ext.hybrid import hybrid_property
from flask_login import UserMixin, current_user
from app.utils import Role, Method
from sqlalchemy.orm import Load, load_only
from sqlalchemy.sql.expression import literal_column
import meta

class Users(db.Model, meta.ResourceMixin, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(255), unique=True)

    oauthId = db.Column(db.String(50))
    oauthProvider = db.Column(db.String(50))

    firstName = db.Column(db.String(50))
    lastName = db.Column(db.String(50))

    password = db.Column(db.String(255))

    avatarPath = db.Column(db.String(255), default='avatar.jpg')
    dateJoined = db.Column(db.DateTime(), default=datetime.utcnow)

    role = db.Column(db.String(), default=Role.USER)

    articles = db.relationship('Articles', backref='users', lazy='dynamic')
    comments = db.relationship('Comments', backref='users', lazy='dynamic')

    _relationships = ('articles', 'comments')

    def __init__(self, **kwargs):
        password = kwargs.pop('password')
        self.set_password(password)
        super(Users, self).__init__(**kwargs)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

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

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    @classmethod
    def get_admin_columns(cls, method):
        return tuple(Users.__mapper__.columns.keys()) + ('password',)

    @classmethod
    def get_guest_columns(cls, method):
        if method == Method.CREATE:
            return 'username', 'email', 'firstName', 'lastName', 'password'
        if method == Method.READ:
            return 'id', 'username', 'firstName', 'lastName', 'avatarPath'
        if method == Method.UPDATE:
            return None
        if method == Method.DELETE:
            return None
        raise RuntimeError('Unknown METHOD: {}'.format(method))

    @classmethod
    def get_user_columns(cls, method):
        if method == Method.CREATE:
            return None
        if method == Method.READ:
            return 'id', 'email', 'username', 'firstName', 'lastName', 'avatarPath', 'role'
        if method == Method.UPDATE:
            return 'email', 'firstName', 'lastName', 'avatarPath', 'password'
        if method == Method.DELETE:
            return None
        raise RuntimeError('Unknown METHOD: {}'.format(method))
