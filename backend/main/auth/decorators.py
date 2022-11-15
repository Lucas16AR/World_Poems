from functools import wraps
from .. import jwt
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def admin_required(fn):
    
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['role'] == 'admin':
            return fn(*args, **kwargs)
        else:
            return 'Only admin users are allowed', 403
    return wrapper

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id

@jwt.additional_claims_loader
def add_claims_to_access_token(user):
    return {'id': user.id, 'role': user.role, 'email': user.email}