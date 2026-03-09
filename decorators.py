from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask import abort
from ..models import User

def admin_required(fn):
    """
    Decorator to allow only admin users (example: user_id==1)
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = int(get_jwt_identity())
        if user_id != 1:  
            abort(403, description="Admin access required")
        return fn(*args, **kwargs)
    return wrapper
