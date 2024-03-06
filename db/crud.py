from werkzeug.security import generate_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .schema import UserModelSchema
from fastapi import HTTPException
from .models import UserModel
from sqlalchemy import select


# 用户模型增删改查
class UserModelCrud:
    # 创建用户
    @staticmethod
    async def create_user(db: AsyncSession, user: UserModelSchema):
        try:
            # 使用异步事务进行操作
            async with db.begin():
                print("路由中获取的数据:", user)
                select_user, msg = await UserModelCrud.get_user(db=db, user_account=user.account)
                if select_user:
                    raise HTTPException(status_code=400, detail={"code": 401,
                                                                 "success": False,
                                                                 "msg": "用户已存在"})
                #  创建用户模型对象
                db_user = UserModel(account=user.account, password=generate_password_hash(user.password),
                                    name=user.name, age=user.age)
                # 将用户对象添加到数据库会话
                db.add(db_user)
                # 提交事务
            await db.commit()
            return True, {"code": 200,
                          "success": False,
                          "msg": "用户创建成功"}
        except IntegrityError:
            return False, {"code": 500,
                           "success": False,
                           "msg": "服务器错误"}

    # 获取单个用户
    @staticmethod
    async def get_user(user_account: str, db: AsyncSession):
        # 使用异步 SQL 查询语句
        select_user = select(UserModel).where(UserModel.account == user_account)
        select_user = await db.execute(select_user)
        # 执行查询并返回结果
        result = select_user.scalar()
        if result:
            user_info = {
                'account': result.account,
                'password': result.password,
                'name': result.name,
                'age': result.age,
            }
            return True, user_info
        return False, {}
