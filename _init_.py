from flask import Flask
from config import Config
from .extensions import db, jwt, api

from .auth.routes import UserRegister, UserLogin
from .tasks.routes import TaskList, TaskDetail

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    api.init_app(app)

    api.add_resource(UserRegister, "/register")
    api.add_resource(UserLogin, "/login")
    api.add_resource(TaskList, "/tasks")
    api.add_resource(TaskDetail, "/tasks/<int:task_id>")

    with app.app_context():
        db.create_all()

    return app
