from datetime import datetime
import uuid
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from sqlalchemy import func

db = SQLAlchemy()
bcrypt = Bcrypt()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), index=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(200))
    creditcard = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.now)
    tokens = db.relationship('Token', backref='user', lazy='dynamic')
    checkins = db.relationship('Checkin', backref='user', lazy='dynamic')

    def __init__(self, email, password, name, creditcard):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.name = name
        self.creditcard = creditcard

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def json(self):
        token = self.tokens.first()
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'token': token.json() if token else None
        }

    def add_token(self, token):
        self.tokens.append(token)


class Token(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self):
        self.id = str(uuid.uuid4())

    def json(self):
        return self.id


class CarPark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    capacity = db.Column(db.Integer)
    free = db.Column(db.Integer, index=True)
    location = db.Column(Geometry())
    address = db.Column(db.String(200))
    cost = db.Column(db.DECIMAL, default=5.0)

    def __init__(self, name, capacity, free, longitude, latitude, address):
        self.name = name
        self.capacity = capacity
        self.free = free
        self.location = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4269)
        self.address = address

    def json(self, lonlat=None):
        o = {
            'id': self.id,
            'name': self.name,
            'type': 0,
            'image': 'http://placehold.it/350x150',
            'capacity': self.capacity,
            'free': self.free,
            'address': self.address,
            'cost': float(self.cost),
            'latitude': db.session.scalar(func.ST_X(self.location)),
            'longitude': db.session.scalar(func.ST_Y(self.location)),
            'distance': None
        }
        if lonlat and len(lonlat) == 2:
            longitude, latitude = lonlat
            o['distance'] = db.session.scalar(
                func.ST_Distance_Sphere(CarPark.location, func.ST_MakePoint(longitude, latitude)))
        return o


class Checkin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkin = db.Column(db.DateTime, default=datetime.now)
    checkout = db.Column(db.DateTime, default=None, nullable=True)
    duration = db.Column(db.Integer)
    cost = db.Column(db.DECIMAL)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    carpark_id = db.Column(db.Integer, db.ForeignKey('car_park.id'))
    carpark = db.relationship('CarPark', backref=db.backref('checkins', lazy='dynamic'))

    def __init__(self, user, car_park):
        self.user_id = user.id
        self.car_park = car_park

    def checkout_now(self):
        self.checkout = datetime.now()
        duration = self.checkout - self.checkin
        self.duration = (duration.days * 60 * 24 + duration.seconds / 60)
        self.cost = duration * self.carpark.cost

    def json(self):
        return {
            'id': self.id,
            'checkin': self.checkin,
            'checkout': self.checkout,
            'duration': self.duration,
            'cost': self.cost,
            'user': self.user.json(),
            'carpark': self.carpark.json()
        }
