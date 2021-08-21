import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen
import os

AUTH0_DOMAIN = os.environ['DATABASE_URL']
ALGORITHMS = os.environ['ALGORITHMS']
API_AUDIENCE = os.environ['API_AUDIENCE']

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header

def get_token_auth_header():
    # Get authorization headers
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError('Authorization header missing', 401)

    # Split headers
    try:
        parts = auth.split()
    except:
        raise AuthError('Malformed header', 401)

    # Error handling
    if parts[0].lower() != 'bearer':
        raise AuthError('Invalid header: must be of type "Bearer"', 401)
    elif len(parts) == 1:
        raise AuthError('Invalid header: authorization token missing', 401)
    elif len(parts) > 2:
        raise AuthError(
            'Invalid header: authorization header must be bearer token', 401
            )
    else:
        # Return token part of header
        return parts[1]


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError('Bad request: permissions not included', 400)
    elif permission not in payload['permissions']:
        raise AuthError('Forbidden', 403)
    else:
        return True


def verify_decode_jwt(token):

    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError('Malformed header', 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError('Token expired', 401)

        except jwt.JWTClaimsError:
            raise AuthError(
                'Incorrect claims. Please check the audience and issuer.', 401
                )

        except Exception:
            raise AuthError(
                'Invalid header: unable to parse authentication token', 400
                )

    raise AuthError('Invalid header: unable to find the appropriate key', 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator