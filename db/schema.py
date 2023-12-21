from pydantic import BaseModel


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
