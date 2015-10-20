from app.extensions import db


class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    
    posts = db.relationship('Posts', backref='category', lazy='dynamic')
