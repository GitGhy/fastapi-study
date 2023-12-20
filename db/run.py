# 在不需要迁移工具的情况下，创建数据库表


from database import engine
from models import Base
import asyncio


# 创建表
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def main():
    await create_tables()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
