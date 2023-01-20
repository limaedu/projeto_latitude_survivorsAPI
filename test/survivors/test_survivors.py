from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base, get_db

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

data = {
    "name" : "foo",
    "gender" : "string",
    "latitude" : 0,
    "longitude" : 0,
}

def test_get_all_survivors():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post("/survivors", json = data)
    response = client.get("/survivors")

    assert response.status_code == 200
    assert response.json() == [{**data, "id": 1, "infected": False}]


def test_get_survivor_by_id():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response_post = client.post("/survivors", json = data)
    id = response_post.json()["id"]

    response_get = client.get(f"/survivors/{id}")

    assert response_get.status_code == 200
    assert response_get.json() == {**data, "id": 1, "infected": False}
    

def test_get_closest_survivor():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post("/survivors", json = data)
    response_post = client.post("/survivors", json = {
    "name" : "bar",
    "gender" : "string",
    "latitude" : 0,
    "longitude" : 0,
    })

    id = response_post.json()["id"]

    response_get = client.get(f"/survivors/distances/{id}")

    assert response_get.status_code == 200
    assert response_get.json() == {**data, "id": 1, "infected": False}


def test_mark_as_infected():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post("/survivors", json = data)
    client.patch("/survivors/1")
    client.patch("/survivors/1")
    response = client.patch("/survivors/1")
    
    assert response.status_code == 200
    assert response.json()["infected"] == True
    

def test_update_survivor():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post("/survivors", json = data)
    new_data = data.copy()
    new_data["name"] = "bar"
    response = client.put("/survivors/1", json = new_data)

    assert response.status_code == 200
    assert response.json() == {**data,"id": 1, "name": "bar", "infected": False,}


def test_create_survivor():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post("/survivors", json = data)

    assert response.status_code == 201
    assert response.json() == {**data, "id": 1, "infected": False}

    