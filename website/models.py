from . import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    firstName = db.Column(db.String(100))
    referralCode = db.Column(db.String(5), unique=True, nullable=False)


class Referral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    referrer_email = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    referred_email = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
