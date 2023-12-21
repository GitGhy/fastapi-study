from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 数据库配置
db_user = 'root'
db_password = '12345678'
db_host = 'localhost'
db_port = '3306'
db_name = 'fastapi_study'
# 数据库连接
SQLALCHEMY_DATABASE_URL = (
    f"mysql+aiomysql://"
    f"{db_user}:{db_password}@{db_host}:{db_port}/{db_name}?charset=utf8")
# 创建数据库引擎
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_size=25, max_overflow=50)
# 创建异步会话
SessionLocal = async_sessionmaker(class_=AsyncSession, autocommit=False, autoflush=False, bind=engine)
# 创建基类
Base = declarative_base()


async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
