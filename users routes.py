from flask_restful import Resource, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import User
from .schemas import user_fields

class UserProfile(Resource):
    @jwt_required()
    @marshal_with(user_fields)
    def get(self):
        """
        Get current logged-in user profile
        """
        user_id = get_jwt_identity()
        user = User.query.get_or_404(user_id)
        return user

class UserList(Resource):
    @jwt_required()
    @marshal_with(user_fields)
    def get(self):
        """
        Get list of all users (admin use)
        """
        users = User.query.all()
        return users
