from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 数据库配置
DB_USER = 'root'
DB_PASSWORD = '12345678'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'fastapi_study'

# 数据库连接
SQLALCHEMY_DATABASE_URL = (
    f"mysql+aiomysql://"
    f"{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8")

# 创建数据库引擎
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, pool_size=25, max_overflow=50)
# 创建异步会话
SessionLocal = async_sessionmaker(class_=AsyncSession, autocommit=False, autoflush=False, bind=engine)
# 创建基类
Base = declarative_base()


# 异步数据库上下文
async def get_db() -> AsyncSession:
    # 使用异步上下文管理器创建数据库会话对象
    async with SessionLocal() as db:
        try:
            yield db  # 返回数据库会话对象
        finally:
            await db.close()  # 关闭数据库会话
