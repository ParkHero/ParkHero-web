from functools import wraps
from flask import Flask, render_template, request, jsonify, g
import requests
from models import db, CarPark, User, bcrypt, Token, Checkin
from sqlalchemy import func

app = Flask(__name__)
app.config.from_object('settings')
db.init_app(app)
bcrypt.init_app(app)

JSON_URL = 'http://data.stadt-zuerich.ch/ogd.GnEZFYm.link'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/install')
def install():
    db.drop_all()
    db.create_all()
    # Load JSON
    r = requests.get(JSON_URL)
    data = r.json()
    for phfeature in data['features']:
        props = phfeature['properties']
        longitude = phfeature['geometry']['coordinates'][0]
        latitude = phfeature['geometry']['coordinates'][1]
        carpark = CarPark(props['Name'], props['oeffentlich'], props['oeffentlich'], longitude, latitude,
                          props['Adresse'])
        db.session.add(carpark)
    db.session.commit()
    return 'DONE'


@app.route('/users/register', methods=['post'])
def users_register():
    if request.get_json() is not None:
        data = request.get_json()
        # Check for required parameters
        required_parameters = ['email', 'password', 'name', 'creditcard']
        for required_parameter in required_parameters:
            if not required_parameter in data:
                return jsonify(error="Required parameters \"{0}\" is missing".format(required_parameter)), 400
        user = User(data['email'], data['password'], data['name'], data['creditcard'])
        token = Token()
        user.add_token(token)
        db.session.add(user)
        db.session.add(token)
        db.session.commit()
        return jsonify(user=user.json())
    return 'NO HTML YET'


@app.route('/users/login', methods=['post'])
def users_login():
    if request.get_json() is not None:
        data = request.get_json()
        # Check for required parameters
        required_parameters = ['email', 'password']
        for required_parameter in required_parameters:
            if not required_parameter in data:
                return jsonify(error="Required parameters \"{0}\" is missing".format(required_parameter)), 400
        user = User.query.filter_by(email=data['email']).first()
        if user is None or not user.check_password(data['password']):
            return jsonify(error="Invalid credentials"), 400
        return jsonify(user=user.json())
    return 'NO HTML YET'


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST':
            data = request.get_json()
        else:
            data = request.args

        token = None
        if data is not None and 'token' in data:
            token = Token.query.filter_by(id=data['token']).first()
        if token is None:
            return jsonify(error="Required parameters \"token\" is missing or invalid"), 400
        g.user = token.user
        return f(*args, **kwargs)

    return decorated_function


@app.route('/carparks')
@token_required
def carparks_list():
    data = request.args

    required_parameters = ["latitude", "longitude"]
    for required_parameter in required_parameters:
        if not required_parameter in data:
            return jsonify(error="Required parameters \"{0}\" is missing".format(required_parameter)), 400
    longitude = data["longitude"]
    latitude = data["latitude"]
    distance = 1000
    carpark_list = CarPark.query.filter(
        func.ST_Distance_Sphere(CarPark.location, func.ST_MakePoint(longitude, latitude)) < distance).all()
    return jsonify(carparks=[cp.json() for cp in carpark_list])


@app.route('/carparks/<carpark_id>/checkin', methods=['post'])
@token_required
def carparks_checkin(carpark_id):
    carpark = CarPark.get_or_404(carpark_id)
    checkin = Checkin(g.user, carpark)
    db.session.add(checkin)
    db.session.commit()
    return jsonify(carpark=carpark.json(), spot=None)


@app.route('/carparks/<carpark_id>/checkout', methods=['post'])
@token_required
def carparks_checkout(carpark_id):
    carpark = CarPark.get_or_404(carpark_id)
    checkin = carpark.checkins.filter_by(user_id=g.user.id).first_or_404()
    checkin.checkout_now()
    db.session.commit()
    return jsonify(carpark=carpark.json(), duration=checkin.duration, cost=checkin.cost)


if __name__ == '__main__':
    app.run()
