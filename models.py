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
    type = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    free = db.Column(db.Integer, index=True)
    free_last_update = db.Column(db.DateTime, default=datetime.now)
    location = db.Column(Geometry())
    address = db.Column(db.String(200))
    cost = db.Column(db.Integer)
    image = db.Column(db.String(500))

    @staticmethod
    def nearby(longitude, latitude, distance):
        return CarPark.query.add_column(
            func.ST_X(CarPark.location).label('longitude')).add_column(
            func.ST_Y(CarPark.location).label('latitude')).add_column(
            func.ST_Distance_Sphere(CarPark.location, func.ST_MakePoint(longitude, latitude)).label('distance')).filter(
            func.ST_Distance_Sphere(CarPark.location, func.ST_MakePoint(longitude, latitude)) <= distance)

    def __init__(self, name, type, capacity, free, cost, longitude, latitude, address, image):
        self.name = name
        self.type = type
        self.capacity = capacity
        self.free = free
        self.cost = cost
        self.location = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4269)
        self.address = address
        self.image = image

    def json(self, longitude=None, latitude=None, distance=None):
        return {
            'id': self.id,
            'name': self.name,
            'type': 0,
            'image': self.image,
            'capacity': self.capacity,
            'free': self.free,
            'free_last_update': self.free_last_update.isoformat(),
            'address': self.address,
            'cost': self.cost,
            'latitude': latitude if latitude else 0,
            'longitude': longitude if longitude else 0,
            'distance': distance if distance else 0
        }


class Checkin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    checkin = db.Column(db.DateTime, default=datetime.now)
    checkout = db.Column(db.DateTime, default=None, nullable=True)
    duration = db.Column(db.Integer)
    cost = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    carpark_id = db.Column(db.Integer, db.ForeignKey('car_park.id'))
    carpark = db.relationship('CarPark', backref=db.backref('checkins', lazy='dynamic'))

    def __init__(self, user, carpark):
        self.user = user
        self.carpark = carpark

    def checkout_now(self):
        self.checkout = datetime.now()
        duration = self.checkout - self.checkin
        self.duration = (duration.days * 60 * 24 + duration.seconds / 60)
        self.cost = int(self.duration / 60.0 * self.carpark.cost)

    def json(self):
        return {
            'id': self.id,
            'checkin': self.checkin.isoformat(),
            'checkout': self.checkout.isoformat(),
            'duration': self.duration,
            'cost': self.cost,
            'user': self.user.json(),
            'carpark': self.carpark.json()
        }
