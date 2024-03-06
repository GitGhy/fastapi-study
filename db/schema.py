from pydantic import BaseModel


# 用户验证模型
class UserModelSchema(BaseModel):
    name: str
    age: int
    account: str
    password: str

# 登录验证模型
class UserLoginSchema(BaseModel):
    """
    User Login Schema
    """
    account: str
    password: str
