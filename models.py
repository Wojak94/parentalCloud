from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import TIME
import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    key = db.Column(db.Integer, unique=True)

    zones = db.relationship('Zone', backref='user')
    locations = db.relationship('Location', backref='user')

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id = id).first()

    def __repr__(self):
        return '<User %r>' % self.name

class Zone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    latitude = db.Column(db.String(48))
    longitude = db.Column(db.String(48))
    radius = db.Column(db.Integer)
    dateStart = db.Column(db.DateTime)
    dateEnd = db.Column(db.DateTime)
    timeStart = db.Column(TIME)
    timeEnd = db.Column(TIME)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Zone %r>' % self.name

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(48))
    longitude = db.Column(db.String(48))
    dateTime = db.Column(db.DateTime)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Location %r>' % self.id

#Association table for Admin-User many-to-many relationship
admin_user = db.Table('admin_user',
    db.Column('adminId', db.Integer, db.ForeignKey('admin.id')),
    db.Column('userId', db.Integer, db.ForeignKey('user.id'))
)

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))

    users = db.relationship('User', secondary=admin_user, backref='admin')

    def __repr__(self):
        return '<Admin %r>' % self.name
