from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


# unique=True, 唯一，nullable=True可空

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(20), nullable=False)
    age = Column(Integer)
    account = Column(String(50), unique=True, nullable=False)
    password = Column(String(500), nullable=False)
    join_time = Column(DateTime, default=datetime.now)


