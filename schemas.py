from flask_restful import fields

task_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "description": fields.String,
    "status": fields.String,
    "priority": fields.Integer,
    "due_date": fields.DateTime(dt_format="iso8601"),
    "user_id": fields.Integer
}
