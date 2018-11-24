from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import TIME
import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    zones = db.relationship('Zone', backref='user')
    locations = db.relationship('Location', backref='user')

    def __repr__(self):
        return '<User %r>' % self.name

class Zone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    latitude = db.Column(db.String(48), unique=True)
    longitude = db.Column(db.String(48), unique=True)
    radius = db.Column(db.Integer, unique=True)
    dateStart = db.Column(db.DateTime, unique=True)
    dateEnd = db.Column(db.DateTime, unique=True)
    timeStart = db.Column(TIME, unique=True)
    timeEnd = db.Column(TIME, unique=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Zone %r>' % self.name

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(48), unique=True)
    longitude = db.Column(db.String(48), unique=True)
    dateTime = db.Column(db.DateTime, unique=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Location %r>' % self.id

#Association table for Admin-User many-to-many relationship
admin_user = db.Table('admin_user',
    db.Column('adminId', db.Integer, db.ForeignKey('admin.id')),
    db.Column('userId', db.Integer, db.ForeignKey('user.id'))
)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)

    users = db.relationship('User', secondary=admin_user, backref='admin')

    def __repr__(self):
        return '<Admin %r>' % self.name
