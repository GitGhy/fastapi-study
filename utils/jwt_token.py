from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from datetime import datetime
import pytz
import jwt

JWT_ALGORITHM = 'HS256'  # JWT算法
SECRET_KEY = "your_secret_key"  # 密钥
TIMEZONE = 'Asia/Shanghai'  # 设置时区为亚洲/上海
EXPIRATION_DAYS = 360000  # Token 过期天数

# 创建时区对象
TZ = pytz.timezone(TIMEZONE)
# 获取当前时间戳
INITIAL_TIME = int(datetime.now(TZ).timestamp())


class JWTToken(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        # 调用基类的构造函数
        super(JWTToken, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        # 从请求头中获取token
        token = request.headers.get('token')
        if not token:
            raise HTTPException(status_code=403, detail='请提供token')

        # 解码token
        decoded_token = self.check_token(token)
        if decoded_token == 'overdue':
            raise HTTPException(status_code=403, detail='token已过期')
        if not decoded_token:
            raise HTTPException(status_code=403, detail=['无效的token'])
        # 返回解码后的token
        return decoded_token

    @staticmethod
    def generate_token(payload: dict) -> str:
        # 过期时间为初始时间加上指定天数的秒数
        expiry = INITIAL_TIME + EXPIRATION_DAYS
        # 将过期时间添加到payload中
        payload['expiry'] = expiry
        try:
            # 生成token
            token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
            return token
        except jwt.PyJWTError as e:
            # 处理JWT库异常，抛出HTTP 500异常
            raise HTTPException(status_code=500, detail=f"{'生成Token时发生错误'}: {str(e)}")

    @staticmethod
    def check_token(token: str):
        try:
            # 解码token并验证签名
            payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            # 获取token中的过期时间
            expiry = payload['expiry']
            # 如果初始时间大于过期时间，则返回overdue表示过期
            if INITIAL_TIME > expiry:
                return "overdue"
            # 返回token
            return payload
        except jwt.InvalidTokenError:
            # 处理无效Token异常，返回False
            return False
