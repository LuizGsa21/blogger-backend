from app.extensions import db
from flask import url_for
from app.utils import Role, Method
import meta

class Categories(db.Model, meta.ResourceMixin):
    __tablename__ = 'categories'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    
    articles = db.relationship('Articles', backref='categories', lazy='dynamic')

    _relationships = ('articles',)

    @property
    def url(self):
        return url_for('categories.get_category_by_id', id=self.id, _external=True)

    @classmethod
    def get_guest_columns(cls, method):
        if method == Method.READ:
            return cls.all_columns
        return None

    @classmethod
    def get_user_columns(cls, method):
        if method == Method.READ:
            return cls.all_columns
        return None
