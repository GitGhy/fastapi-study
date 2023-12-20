from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import engine_from_config
from logging.config import fileConfig
from alembic import context
from sqlalchemy import pool
from db.models import Base
import asyncio

# 获取 Alembic 配置对象，它提供了对正在使用的 .ini 文件中的值的访问。
config = context.config

# 解释用于 Python 日志记录的配置文件。
# 此行基本上设置了日志记录器。
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 在这里添加你的模型的 MetaData 对象
target_metadata = Base.metadata


# 从配置中获取的其他值，由 env.py 的需要定义：
# my_important_option = config.get_main_option("my_important_option")


# 离线运行迁移
def run_migrations_offline() -> None:
    # 获取数据库连接 URL
    url = config.get_main_option("sqlalchemy.url")

    # 配置 Alembic 上下文
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    # 在事务中执行迁移
    with context.begin_transaction():
        context.run_migrations()


# 在连接上运行迁移的函数
def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    # 在事务中执行迁移
    with context.begin_transaction():
        context.run_migrations()


# 异步运行在线迁移
async def run_migrations_online():
    # 创建异步数据库引擎
    connectable = AsyncEngine(
        engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True,
        )
    )

    # 使用连接运行迁移
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


# 如果处于离线模式，则运行离线迁移
if context.is_offline_mode():
    run_migrations_offline()
else:
    # 否则，运行在线异步迁移
    asyncio.run(run_migrations_online())
