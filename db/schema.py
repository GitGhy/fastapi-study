from pydantic import BaseModel


# 数据验证模型
class UserModelSchema(BaseModel):
    name: str
    age: int
    account: str
    password: str


class UserLoginSchema(BaseModel):
    """
    User Login Schema
    """
    account: str
    password: str
