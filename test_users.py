import pytest
from app import create_app
from app.extensions import db
from app.models import User
from flask_jwt_extended import create_access_token

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    with app.app_context():
        db.create_all()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def token(app):
    with app.app_context():
        user = User(username="charlie", password_hash="fakehash")
        db.session.add(user)
        db.session.commit()
        return create_access_token(identity=str(user.id))

def test_user_profile(client, token):
    headers = {"Authorization": f"Bearer {token}"}

    res = client.get("/users/profile", headers=headers)
    assert res.status_code == 200
    assert res.json["username"] == "Suresh"
