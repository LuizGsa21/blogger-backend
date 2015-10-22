from app.extensions import db


class Categories(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    
    articles = db.relationship('Articles', backref='category', lazy='dynamic')
