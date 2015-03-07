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
    tokens = db.relationship('Token', backref='user', lazy='dynamic')

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
    slots = db.Column(db.Integer)
    slots_free = db.Column(db.Integer, index=True)
    location = db.Column(Geometry())
    address = db.Column(db.String(200))

    def __init__(self, name, slots, slots_free, longitude, latitude, address):
        self.name = name
        self.slots = slots
        self.slots_free = slots_free
        self.location = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4269)
        self.address = address
