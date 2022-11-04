from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app=app)


"""def test_root():
    response = client.get("/")
    assert response.status_code == 404
    # assert response.json() == {"message": "Hello World"}"""
