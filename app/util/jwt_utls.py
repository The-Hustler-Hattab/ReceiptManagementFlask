from functools import wraps

from authlib.jose import jwt
from flask import request, jsonify

from app import OKTA_JWK_URL, app, Constants
from security import safe_requests


def get_okta_public_keys():
    response = safe_requests.get(OKTA_JWK_URL)
    response.raise_for_status()
    return response.json()['keys']


keys = get_okta_public_keys()


def verify_jwt(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token or not token.startswith('Bearer '):
            return jsonify({'message': 'Missing or invalid token format'}), 401

        token = token.split(' ')[1]
        # Try decoding token using each key until successful
        for key in keys:
            try:
                jwt.decode(token, key)

                # If token is valid, proceed with the request
                return f(*args, **kwargs)
            except Exception as e:
                print(e)
                # Ignore any errors during decoding and try the next key
                pass

        # If none of the keys succeeded in decoding the token, return an error
        return jsonify({'message': 'Invalid token'}), 401

    return decorated_function


def verify_token_and_role(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print("Verify token and role")
        token = request.headers.get('Authorization')

        if not token or not token.startswith('Bearer '):
            return jsonify({'message': 'Missing or invalid token format'}), 401

        token = token.split(' ')[1]
        for key in keys:
            try:
                decoded_token = jwt.decode(token, key)
                user_roles = decoded_token.get('user-role', [])
                if app.config.get(Constants.ADMIN_GROUP) in user_roles:
                    return f(*args, **kwargs)
                else:
                    return jsonify({'message': 'Forbidden: User does not have the required role'}), 403
            except Exception as e:
                print(e)
                pass

        return jsonify({'message': 'Invalid token'}), 401

    return decorated_function


def get_jwt() -> str:
    token = request.headers.get('Authorization')
    return token.split(' ')[1]


def get_decoded_token() -> dict:
    token = get_jwt()
    for key in keys:
        try:
            return jwt.decode(token, key)
        except Exception as e:
            print(e)
            pass
    return {}


def get_full_name():
    decoded_token = get_decoded_token()
    full_name = decoded_token.get('UserFullName')
    return full_name
