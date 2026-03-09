from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = "sqlite:///task_manager.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = ''
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
