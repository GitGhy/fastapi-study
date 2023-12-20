import requests
import uvicorn
import socket
import re


# 获取本机公网IP
def get_ip_public():
    try:
        response = requests.get("https://txt.go.sohu.com/ip/soip")
        response.raise_for_status()  # 抛出异常如果HTTP请求返回不成功
        ip_public = re.search(r'\d+\.\d+\.\d+\.\d+', response.text).group()
        server_info = f"INFO:     Uvicorn running on http://{ip_public}:8000 (Press CTRL+C to quit)"
        print(server_info)
        return server_info
    except requests.RequestException as e:
        print(f"无法获取IP: {e}")
        return e


# 获取本机局域网IP
def local_ip():
    # 若使用网络代理，则代码无效
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]

        server_info = f"INFO:     Uvicorn running on http://{ip}:8000 (Press CTRL+C to quit)"
        print(server_info)
        return server_info
    except Exception as e:
        print(f"无法获取IP: {e}")
        return e


if __name__ == "__main__":
    # app = local_ip()
    print(f"INFO:     Uvicorn running on http://192.168.1.102:8000 (Press CTRL+C to quit)")
    uvicorn.run(app='main:app', host="0.0.0.0", port=8000, reload=True)
