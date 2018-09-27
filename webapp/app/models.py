from app import db
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash


class Account(db.Model):
    """
    Account table represents a user in the database
    The account id will be used as a representation of the account

    """
    __tablename__ = 'account'

    id = db.Column(Integer, primary_key=True)
    user = db.Column(db.String(254), unique=True)
    password = db.Column(db.String(255))
    recordings = db.relationship("Recordings", backref="account")

    def __repr__(self):
        return '<User: %r>' % (self.user)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


class Recordings(db.Model):

    __tablename__ = 'recordings'

    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('account.id'))
    name = db.Column(db.String(254), unique=True)
    track_length = db.Column(db.String(254), unique=True)

    def __repr__(self):
        return '<Recording: %r>' % (self.name)
