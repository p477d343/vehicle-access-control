import jwt
from .config import SECRET_KEY

def generate_token(vehicle_id):
    payload = {
        'vehicle_id': vehicle_id
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def validate_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        vehicle_id = payload['vehicle_id']
        return vehicle_id
    except jwt.exceptions.InvalidTokenError:
        return None