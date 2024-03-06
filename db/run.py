# 在不需要迁移工具的情况下，创建数据库表，仅适用于不会更新数据库的生产环境
from database import engine
from models import Base
import asyncio


# 创建表
async def create_tables():
    # 使用数据库引擎创建连接
    async with engine.begin() as conn:
        # 在连接上同步创建所有表
        await conn.run_sync(Base.metadata.create_all)


# 执行创建表的异步函数
async def main():
    await create_tables()


# 获取事件循环对象
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
