import json
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'fsndmms.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffee'

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    #print(jsonurl)
    jwks = json.loads(jsonurl.read())
    #print(jwks)
    unverified_header = jwt.get_unverified_header(token)
    #print(unverified_header)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

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
            #print(token)
            #print(rsa_key)
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            print(payload)
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImhteEJXUVdrRTlxR094UDI4eVJXSSJ9.eyJpc3MiOiJodHRwczovL2ZzbmRtbXMudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY1YzIyZTI3NThmMTQxYjRjYTFkNmFjZiIsImF1ZCI6ImNvZmZlZSIsImlhdCI6MTcwODYzODk3MCwiZXhwIjoxNzA4NjQ2MTcwLCJhenAiOiJabzhRREgxeGIzcXQyMWpmYXNSZ1c2VUV5bFExUzVYYyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmRyaW5rcyIsImdldDpkcmlua3MtZGV0YWlsIl19.QXOIshJobCU5MhD8dhlnK6vL-jKKjLkItig7v5ZoTnUQr8ZM5tovFbuBlqyVq0QweMRHrrsPs-407J2rT_g3R7y8EZxS8OBmfsN5kpWqrVv4l01QjhR95x6htwSC0eCxYYslYeODZ-W_tpLLs916086rhujQy0y372s_nA7ljc3jn3slBheXrXiiD_QZbQGbrzNXrGOM2KAH5ksOeeft5B17wg4Y7z0V9mZ8qYWeMl_1_xIRzPtbN4aC-Rl-tggVCyJ5LSOewzc362H3HI7vkM-fo5uFkZOWBnMNbh8PO0HVRi_CqgOvvB5arcdavvzXyyh0jcmAnJk76i_briZGWw"
try:
    decoded_payload = verify_decode_jwt(token)
    print(decoded_payload)
except AuthError as e:
    print(f"AuthError: {e.error}")