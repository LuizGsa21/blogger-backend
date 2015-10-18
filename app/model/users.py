from app.extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


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

    avatar_path = db.Column(db.String(255), default='avatar.jpg')
    dateJoined = db.Column(db.DateTime(), default=datetime.utcnow)

    isAdmin = db.Column(db.Boolean(), default=False)

    posts = db.relationship('Posts', backref='author', lazy='dynamic')
    comments = db.relationship('Comments', backref='user', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Users, self).__init__(**kwargs)
        self.pwdhash = generate_password_hash(self.pwdhash)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
