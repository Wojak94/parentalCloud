from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import TIME
from sqlalchemy import desc, func
import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    key = db.Column(db.Integer, unique=True)

    zones = db.relationship('Zone', backref='user')
    locations = db.relationship('Location', backref='users')

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

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<Zone %r>' % self.name

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String(48))
    longitude = db.Column(db.String(48))
    dateTime = db.Column(db.DateTime)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))

    @classmethod
    def get_recent_location(cls, userId):
        x = cls.query.filter_by(userId = userId).order_by(cls.dateTime.desc()).first()
        return {'latitude': x.latitude, 'longitude': x.longitude, 'datetime': x.dateTime.__str__()}

    @classmethod
    def get_locations_by_date(cls, date, id):
        locations = list(cls.query.filter(Location.userId == id).filter(func.DATE(Location.dateTime) == datetime.datetime.strptime(date, '%Y-%m-%d')))
        return locations

    @property
    def serialize(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'dateTime': self.dateTime,
        }

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
