from app.extensions import db
import meta

class Categories(db.Model, meta.ResourceMixin):
    __tablename__ = 'categories'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    
    articles = db.relationship('Articles', backref='categories', lazy='dynamic')
