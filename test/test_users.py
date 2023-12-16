from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)


# @pytest.mark.skip(reason="Skipping due to GZipMiddleware issue")
class TestUser:
    def test_userinfo_valid_data(self):
        # 准备有效的请求数据
        valid_data = {"name": "John Doe", "age": 25}
        # 发送 POST 请求
        response = client.post("/user/userinfo", json=valid_data)
        # 断言状态码为 200
        assert response.status_code == 200
        # 断言返回数据与请求数据一致
        assert response.json() == [{"userinfo": valid_data}]

    def test_userinfo_invalid_data(self):
        # 准备无效的请求数据
        invalid_data = {"name": "", "age": "not_an_int"}
        # 发送 POST 请求
        response = client.post("/user/userinfo", json=invalid_data)
        # 断言状态码为 400
        assert response.status_code == 400
        # 断言错误消息中包含期望的信息
        assert "参数类型为空" in response.text
