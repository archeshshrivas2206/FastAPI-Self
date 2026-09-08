from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_read_root():
    response =client.get("/")
    assert response.status_code==200

def test_register_and_logic():
    response=client.post("/register",json={
        "username":"testuser123",
        "email":"testuser123@example.com","password":"testpassword"
    })
    assert response.status_code==201
    data=response.json()
    assert data["username"]=="testuser123"
    assert "password" not in data
    assert "hashed_password" not in data


    response = client.post("/login",data={
        "username": "testuser123",
        "password": "testpassword"
    })

    assert response.status_code==200
    assert "access_token" in response.json()
    
