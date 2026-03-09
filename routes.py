from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import create_access_token
from ..models import User
from ..extensions import db
from .utils import hash_password, verify_password

class UserRegister(Resource):

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username", required=True)
        parser.add_argument("password", required=True)
        args = parser.parse_args()

        if User.query.filter_by(username=args["username"]).first():
            return {"message": "User already exists"}, 400

        new_user = User(
            username=args["username"],
            password_hash=hash_password(args["password"]),
        )

        db.session.add(new_user)
        db.session.commit()

        return {"message": "User created successfully"}, 201

class UserLogin(Resource):

    def post(self):
        data = request.get_json()

        user = User.query.filter_by(username=data.get("username")).first()

        if user and verify_password(user.password_hash, data.get("password")):
            token = create_access_token(identity=str(user.id))
            return {"access_token": token}, 200

        return {"message": "Invalid credentials"}, 401
