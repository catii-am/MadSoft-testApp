from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from public_api.main import app, get_db
from public_api.database import Base, engine, SessionLocal
from public_api.models import Meme
from sqlalchemy.orm import sessionmaker

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_create_meme():
    responce = client.post("/memes/", json={
        "title": "Test Name",
        "description": "Test description",
        "image": "https://testImage.url/image.jpg"
    })
    assert responce.status_code == 200
    assert responce.json()["title"] == "Test Name"


def test_read_memes():
    response = client.get('/memes/')
    assert response.status_code == 200
    assert len(response.json()["items"]) > 0


def test_read_meme():
    response = client.get('/memes/1')
    assert response.status_code == 200
    assert response.json()["title"] == "Test Name"


def test_update_meme():
    response = client.put("/memes/1", json={
        "title": "Updated Name",
        "description": "Updated description",
        "image": "https://updatedImage.url/image.jpg"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Name"


def test_delete_meme():
    response = client.delete('/memes/1')
    assert response.status_code == 200
    response = client.get('/memes/1')
    assert response.status_code == 404
