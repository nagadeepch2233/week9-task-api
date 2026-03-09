from flask_restful import Resource, reqparse, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request

from ..models import Task
from ..extensions import db
from .schemas import task_fields

class TaskList(Resource):

    @jwt_required()
    @marshal_with(task_fields)
    def get(self):
        user_id = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument("status", type=str, location="args")
        parser.add_argument("page", type=int, default=1, location="args")

        args = parser.parse_args()

        query = Task.query.filter_by(user_id=user_id)

        if args["status"]:
            query = query.filter_by(status=args["status"])

        tasks = query.paginate(page=args["page"], per_page=10).items

        return tasks

    @jwt_required()
    @marshal_with(task_fields)
    def post(self):

        user_id = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument("title", required=True)
        parser.add_argument("description")
        parser.add_argument("priority", type=int)
        parser.add_argument("due_date")

        args = parser.parse_args()

        new_task = Task(
            title=args["title"],
            description=args["description"],
            priority=args["priority"] or 1,
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

        task.title = data.get("title", task.title)
        task.description = data.get("description", task.description)
        task.status = data.get("status", task.status)
        task.priority = data.get("priority", task.priority)

        db.session.commit()

        return task

    @jwt_required()
    def delete(self, task_id):

        user_id = get_jwt_identity()

        task = Task.query.filter_by(id=task_id, user_id=user_id).first_or_404()

        db.session.delete(task)
        db.session.commit()

        return {"message": "Task deleted successfully"}, 200
