from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# --- Configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///task_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = ''
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

db = SQLAlchemy(app)
api = Api(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    tasks = db.relationship('Task', backref='owner', lazy=True)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')  
    priority = db.Column(db.Integer, default=1)           
    due_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

task_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'status': fields.String,
    'priority': fields.Integer,
    'due_date': fields.DateTime(dt_format='iso8601'),
    'user_id': fields.Integer
}

class UserRegister(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="Username is required")
        parser.add_argument('password', required=True, help="Password is required")
        args = parser.parse_args()

        if User.query.filter_by(username=args['username']).first():
            return {"message": "User already exists"}, 400

        hashed_pw = generate_password_hash(args['password'])
        new_user = User(username=args['username'], password_hash=hashed_pw)
        #db.session.add(new_user)
        #db.session.commit()
        return {"message": "User created successfully"}, 201

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        user = User.query.filter_by(username=data.get('username')).first()
        
        if user and check_password_hash(user.password_hash, data.get('password')):
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token}, 200
        
        return {"message": "Invalid credentials"}, 401

class TaskList(Resource):
    @jwt_required()
    @marshal_with(task_fields)
    def get(self):
        user_id = get_jwt_identity()
        
        # Filtering & Pagination logic
        parser = reqparse.RequestParser()
        parser.add_argument('status', type=str, location='args')
        parser.add_argument('page', type=int, default=1, location='args')
        args = parser.parse_args()

        query = Task.query.filter_by(user_id=user_id)
        if args['status']:
            query = query.filter_by(status=args['status'])
        
        # Return paginated items (10 per page)
        tasks = query.paginate(page=args['page'], per_page=10).items
        return tasks

    @jwt_required()
    @marshal_with(task_fields)
    def post(self):
        user_id = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument('title', required=True)
        parser.add_argument('description')
        parser.add_argument('priority', type=int)
        args = parser.parse_args()

        new_task = Task(
            title=args['title'],
            description=args['description'],
            priority=args['priority'] or 1,
            user_id=user_id
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task, 201

class TaskDetail(Resource):
    @jwt_required()
    @marshal_with(task_fields)
    def put(self, task_id):
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
        
        data = request.get_json()
        task.title = data.get('title', task.title)
        task.status = data.get('status', task.status)
        
        db.session.commit()
        return task

    @jwt_required()
    def delete(self, task_id):
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deleted"}, 200

api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(TaskList, '/tasks')
api.add_resource(TaskDetail, '/tasks/<int:task_id>')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize SQLite database
    app.run(debug=True)
