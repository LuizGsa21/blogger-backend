import pprint
from app.extensions import db
from datetime import datetime
from app.utils import Role, Method
import meta
from sqlalchemy.orm import Load, load_only
from flask import url_for


class Articles(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer(), primary_key=True)
    categoryId = db.Column(db.Integer(), db.ForeignKey('categories.id'), nullable=False)
    authorId = db.Column(db.Integer(), db.ForeignKey('users.id'), nullable=False)

    title = db.Column(db.String(255))
    body = db.Column(db.String(20000))
    slug = db.Column(db.String(255))

    dateCreated = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    lastModified = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)

    comments = db.relationship('Comments', backref='articles', lazy='dynamic')

    _relationships = ('users', 'comments', 'categories')

    @property
    def url(self):
        return url_for('articles.get_article_by_id', id=self.id, _external=True)

    @classmethod
    def get_guest_columns(cls, method):
        if method == Method.READ:
            return tuple(Articles.__mapper__.columns.keys())
        else:
            return None

    @classmethod
    def get_user_columns(cls, method):
        all_columns = set(Articles.__mapper__.columns.keys())
        if method == Method.CREATE:
            return all_columns - {'dateCreated', 'lastModified'}
        if method == Method.READ:
            return all_columns
        if method == Method.UPDATE:
            return all_columns - {'dateCreated', 'lastModified'}
        if method == Method.DELETE:
            return all_columns - {'dateCreated', 'lastModified'}
        raise RuntimeError('Unknown METHOD: {}'.format(method))
