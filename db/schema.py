from pydantic import BaseModel


class UserModelSchema(BaseModel):
    name: str
    age: int
    account: str
    password: str

    class Config:
        orm_mode = True
