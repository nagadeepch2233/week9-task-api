import pytest
from app import create_app
from app.extensions import db
from app.models import User

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

def test_register_and_login(client):
  
    res = client.post("/register", json={"username": "alice", "password": "123456"})
    assert res.status_code == 201

    res2 = client.post("/register", json={"username": "alice", "password": "123456"})
    assert res2.status_code == 400

    res3 = client.post("/login", json={"username": "alice", "password": "123456"})
    assert res3.status_code == 200
    assert "access_token" in res3.json

    res4 = client.post("/login", json={"username": "alice", "password": "wrong"})
    assert res4.status_code == 401
