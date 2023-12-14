from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


class TestUser:
    def test_user_name(self):
        response = client.get("/user/ghy")
        print(response.json())
        assert response.status_code == 200
        assert response.json() == [{"username": "ghy"}]

    def test_user_name2(self):
        response = client.get("/user/zzp")
        print(response.json())
        assert response.status_code == 200
        assert response.json() == [{"username": "zzp"}]
