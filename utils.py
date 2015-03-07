from functools import wraps
from flask import request, jsonify, g
from models import Token


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == 'POST':
            data = request.get_json()
        else:
            data = request.args

        token = None
        try:
            token = Token.query.get(data['token'])
            if token is None:
                raise KeyError()
        except (TypeError, KeyError):
            return jsonify(error="Required parameters \"token\" is missing or invalid"), 400
        g.user = token.user
        return f(*args, **kwargs)

    return decorated_function