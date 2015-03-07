from flask import Flask

app = Flask(__name__)
app.config.from_object('settings')


@app.route('/install')
def hello_world():
    return 'TODO!'


@app.route('/users/register', methods=['post'])
def users_register():
    return 'TODO!'


@app.route('/users/login', methods=['post'])
def users_login():
    return 'TODO!'


@app.route('/carparks/list')
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
