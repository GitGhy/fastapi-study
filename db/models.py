from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from db.database import Base


# unique=True, 唯一，nullable=True可空


# 用户表
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    age = Column(Integer)
    account = Column(String(50), unique=True, nullable=False)
    password = Column(String(500), nullable=False)
    join_time = Column(DateTime, default=datetime.now)
