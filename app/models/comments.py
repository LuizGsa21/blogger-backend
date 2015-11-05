from app.extensions import db
from datetime import datetime
import meta

class Comments(db.Model, meta.ResourceMixin):
    __tablename__ = 'comments'

    id = db.Column(db.Integer(), primary_key=True)
    parentId = db.Column(db.Integer(), db.ForeignKey('comments.id'), nullable=True)
    userId = db.Column(db.Integer(), db.ForeignKey('users.id'))
    articleId = db.Column(db.Integer(), db.ForeignKey('articles.id'))

    title = db.Column(db.String(200))
    body = db.Column(db.String(10000))
    likes = db.Column(db.Integer())

    lastModified = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
    dateCreated = db.Column(db.DateTime(), default=datetime.utcnow, nullable=False)
