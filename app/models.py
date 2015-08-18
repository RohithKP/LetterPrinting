from app import db
from datetime import datetime
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(120), index=True, unique=True)
    is_admin = db.Column(db.Boolean(), default=False)
    is_user = db.Column(db.Boolean(), default=False)
    signUp_date = db.Column(db.DateTime)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    author = relationship(User)
    content = db.Column(db.Text)

    def __repr__(self):
        return   "%d/%s/%s" % (self.id, self.username)
