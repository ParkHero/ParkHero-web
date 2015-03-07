from flask import Flask, render_template, request, jsonify
from flask.ext.bcrypt import Bcrypt
import requests
from models import db, CarPark, User, bcrypt, Token

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
    return 'TODO!'


@app.route('/carparks')
def carparks_list():
    return 'TODO!'


@app.route('/carparks/<carpark_uuid>/checkin', methods=['post'])
def carparks_checkin(carpark_uuid):
    return 'TODO!'


@app.route('/carparks/<carpark_uuid>/checkout', methods=['post'])
def carparks_checkout(carpark_uuid):
    return 'TODO!'


if __name__ == '__main__':
    app.run()
