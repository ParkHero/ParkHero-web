import random
from flask import Flask, render_template, request, jsonify, g, url_for
import requests
from models import db, CarPark, User, bcrypt, Token, Checkin, CarParkChoice
from livedata.live_get_collection import LiveGetCollection
from utils import token_required
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object('settings')
db.init_app(app)
bcrypt.init_app(app)

JSON_URL = 'http://data.stadt-zuerich.ch/ogd.GnEZFYm.link'
IMAGES = {
    'Accu': 'img/carparks/accu.jpg',
    'Albisriederplatz': 'img/carparks/albisriederplatz.jpg',
    'Bleicherweg': 'img/carparks/bleicherweg.jpg',
    'Center Eleven': 'img/carparks/center_11.jpg',
    'Central': 'img/carparks/central.jpg',
    'City Parking': 'img/carparks/city.jpg',
    'Cityport': 'img/carparks/cityport.jpg',
    'Crowne Plaza': 'img/carparks/crowne_plaza.jpg',
    'Dorflinde': 'img/carparks/dorflinde.jpg',
    'Feldegg': 'img/carparks/feldegg.jpg',
    'Globus': 'img/carparks/globus.jpg',
    'Hardau II': 'img/carparks/hardau.jpg',
    'Hauptbahnhof': 'img/carparks/hb.jpg',
    'Jelmoli': 'img/carparks/jelmoli.jpg',
    'Jungholz': 'img/carparks/jungholz.jpg',
    'Max Bill-Platz': 'img/carparks/max_bill_platz.jpg',
    'Messe': 'img/carparks/messe.jpg',
    'Nordhaus': 'img/carparks/nordhaus.jpg',
    'Octavo': 'img/carparks/octavo.jpg',
    'Opéra': 'img/carparks/opera.jpg',
    'P West': 'img/carparks/p_west.jpg',
    'Park Hyatt': 'img/carparks/park_hyatt.jpg',
    'Parkside': 'img/carparks/parkside.jpg',
    'Pfingstweid': 'img/carparks/pfingsweid.jpg',
    'Talgarten': 'img/carparks/talgarten.jpg',
    'Universität Irchel': 'img/carparks/uni_irchel.jpg',
    'Urania': 'img/carparks/urania.jpg',
    'Utoquai': 'img/carparks/utoquai.jpg',
    'Züri 11': 'img/carparks/zueri11.jpg',
    'Zürichhorn (Baurstrasse)': 'img/carparks/zuerichhorn.jpg',
}


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
    carparks = []
    for phfeature in data['features']:
        props = phfeature['properties']
        longitude = phfeature['geometry']['coordinates'][0]
        latitude = phfeature['geometry']['coordinates'][1]
        image = IMAGES.get(props['Name'], 'img/carparks/misc.jpg')
        carpark = CarPark(props['Name'], 0, props['oeffentlich'], props['oeffentlich'], random.randint(0, 3) * 100,
                          longitude, latitude, props['Adresse'], image)
        db.session.add(carpark)
        carparks.append(carpark)
    carpark = CarPark('Leonhardshalde', 1, 10, 5, 0, 8.54517, 47.37708, 'Leonhardshalde', 'img/carparks/misc.jpg')
    db.session.add(carpark)
    carparks.append(carpark)
    carpark = CarPark('Clausiusstrasse', 1, 20, 3, 0, 8.54586, 47.37963, 'Clausiusstrasse', 'img/carparks/misc.jpg')
    db.session.add(carpark)
    carparks.append(carpark)
    carpark = CarPark('Huttenstrasse', 1, 5, 5, 0, 8.55139, 47.38012, 'Huttenstrasse', 'img/carparks/misc.jpg')
    db.session.add(carpark)
    carparks.append(carpark)
    # Add default user
    user = User('aaaa', '123456', 'Hans Test', 'test cc')
    db.session.add(user)
    token = Token()
    db.session.add(token)
    for i in range(20):
        checkin = Checkin(user, random.choice(carparks))
        checkin.checkin = datetime.now() - timedelta(seconds=random.randint(10, 300) * 60)
        checkin.checkout_now()
        db.session.add(checkin)
    user.add_token(token)

    db.session.commit()
    return 'DONE'

@app.route('/reload_spots')
def reload_spots():
    live_data = LiveGetCollection()
    i = 0
    for data in live_data.get_all():
        car_park = CarPark.query.filter_by(name=data.name).first()
        if car_park:
            car_park.free = data.free
            car_park.free_last_update = datetime.now()
            i += 1

    db.session.commit()
    return jsonify(updated=str(i))

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

@app.route('/users/update', methods=['post'])
@token_required
def users_update():
    if request.get_json() is not None:
        data = request.get_json()
        # Check for required parameters
        required_parameters = ['email', 'name']
        for required_parameter in required_parameters:
            if not required_parameter in data:
                return jsonify(error="Required parameters \"{0}\" is missing".format(required_parameter)), 400
        g.user.email = data['email']
        g.user.name = data['name']
        if 'password' in data and data['password']:
            g.user.set_password(data['password'])
        if 'creditcard' in data and data['creditcard']:
            g.user.set_password(data['creditcard'])
        db.session.commit()
        return jsonify(user=g.user.json())
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


@app.route('/users/details')
@token_required
def users_details():
    return jsonify(user=g.user.json())


@app.route('/users/checkins')
@token_required
def users_checkins():
    checkins = g.user.checkins.order_by(Checkin.id).all()
    return jsonify(user=g.user.json(), checkins=[checkin.json() for checkin in checkins])


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
    carpark_list = CarPark.nearby(longitude, latitude, distance).all()
    return jsonify(
        carparks=[cp.json(cp_longitude, cp_latitude, cp_distance) for cp, cp_longitude, cp_latitude, cp_distance in
                  carpark_list])


@app.route('/carparks/<carpark_id>/checkin', methods=['post'])
@token_required
def carparks_checkin(carpark_id):
    carpark = CarPark.query.get_or_404(carpark_id)
    checkin = Checkin(g.user, carpark)
    db.session.add(checkin)
    db.session.commit()
    return jsonify(carpark=carpark.json(), spot=None)


@app.route('/carparks/<carpark_id>/checkout', methods=['post'])
@token_required
def carparks_checkout(carpark_id):
    carpark = CarPark.query.get_or_404(carpark_id)
    checkin = carpark.checkins.filter_by(user_id=g.user.id).filter_by(checkout=None).first_or_404()
    checkin.checkout_now()
    db.session.commit()
    return jsonify(carpark=carpark.json(), duration=checkin.duration, cost=checkin.cost)

@app.route('/carparks/<carpark_id>/details')
@token_required
def carparks_details(carpark_id):
    carpark = CarPark.query.get_or_404(carpark_id)
    choice = CarParkChoice(g.user, carpark)
    db.session.add(choice)
    db.session.commit()
    return jsonify(carpark=carpark.json(), user=g.user.json())

if __name__ == '__main__':
    app.run()
