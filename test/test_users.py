from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# @pytest.mark.skip(reason="Skipping due to GZipMiddleware issue")
class TestUser:
    def test_login(self):
        # 准备有效的请求数据
        valid_data = {
            "name": "ghy",
            "age": 21,
            "account": 123,
            "password": "123"
        }
        # 发送 POST 请求
        response = client.post("/user/login", json=valid_data)
        # 断言状态码为 200
        assert response.status_code == 200
        assert response.json()['code'] == 200

    def test_token(self):
        # 准备无效的请求数据
        headers = {
            'token': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJuYW1lIjoiZ2h5IiwiYWdlIjoyMSwiYWNjb3VudCI6MTIzLCJwYXNzd29yZCI6IjEyMyIsImV4cGlyeSI6MTcwMzE2NTMyM30.YwutrfIZtUTZUrgJ16Pzcoqq6MGhQzGQYsH8p7Bmqe0'
        }
        # 发送 POST 请求
        response = client.get("/user/token", headers=headers)
        # 断言状态码为 200
        assert response.status_code == 200
        assert response.json()['code'] == 200
