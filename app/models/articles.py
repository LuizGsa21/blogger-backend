from app.extensions import db
from datetime import datetime

class Articles(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer(), primary_key=True)
    categoryId = db.Column(db.Integer(), db.ForeignKey('categories.id'), nullable=False)
    authorId = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)

    title = db.Column(db.String(255))
    body = db.Column(db.String(20000))
    likes = db.Column(db.Integer())
    slug = db.Column(db.String(255))

    dateCreated = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    lastModified = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)

    comments = db.relationship('Comments', backref='articles', lazy='dynamic')
