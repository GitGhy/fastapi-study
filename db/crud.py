from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from schema import UserModelSchema
from models import UserModel


class UserModelCrud:
    # 创建用户
    @staticmethod
    async def create_user(db: AsyncSession, user: UserModelSchema):
        # 使用异步事务进行操作
        async with db.begin():
            #  创建用户模型对象
            db_user = UserModel(**user.dict())
            # 将用户对象添加到数据库会话
            db.add(db_user)
            # 提交事务
            await db.flush()
            # 刷新数据库
            await db.refresh(db_user)
        return db_user

    # 获取单个用户
    @staticmethod
    async def get_user(db: AsyncSession, user_id: int):
        # 使用异步 SQL 查询语句
        statement = select(UserModel).where(UserModel.id == user_id)
        # 执行查询并返回结果
        result = await db.execute(statement)
        return result.scalar_one_or_none()

    # 获取多个用户
    @staticmethod
    async def get_users(db: AsyncSession, skip: int = 0, limit: int = 10):
        # 使用异步 SQL 查询语句
        statement = select(UserModel).offset(skip).limit(limit)
        # 执行查询并返回所有结果
        result = await db.execute(statement)
        return result.scalars().all()

    # 更新用户信息
    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, new_user: UserModel):
        # 获取要更新的用户
        user_to_update = await UserModelCrud.get_user(db, user_id)
        # 如果找到要更新的用户，则更新其属性
        if user_to_update:
            for key, value in new_user.dict().items():
                setattr(user_to_update, key, value)
            # 使用异步事务提交更改
            await db.flush()
        return user_to_update

    # 删除用户
    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int):
        # 获取要删除的用户
        user_to_delete = await UserModelCrud.get_user(db, user_id)
        # 如果找到要删除的用户，则执行删除操作
        if user_to_delete:
            async with db.begin():
                await db.delete(user_to_delete)
                # 使用异步事务提交更改
                await db.flush()
        return {"message": "用户删除成功"}
