from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestOne:
    def test_task_one(self):
        response = client.get("/task/one")
        print(response.json())
        assert response.status_code == 200
        assert response.json() == [{"username": "g"}, {"username": "?"}]

    def test_task_two(self):
        response = client.post("/task/two")
        print(response.json())
        assert response.status_code == 200
        assert response.json() == {"method": "post"}
