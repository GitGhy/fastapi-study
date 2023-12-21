from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from .schema import UserModelSchema
from .models import UserModel


class UserModelCrud:
    # 创建用户
    @staticmethod
    async def create_user(db: AsyncSession, user: UserModelSchema):
        try:
            # 使用异步事务进行操作
            async with db.begin():
                print("hh", user.dict())
                user_info = user.dict()
                print(user_info['account'])
                select_user, msg = await UserModelCrud.get_user(db=db, user_account=user_info['account'])
                print(select_user)
                if select_user:
                    raise HTTPException(status_code=400, detail={"code": 401,
                                                                 "success": False,
                                                                 "msg": "用户已存在"})
                #  创建用户模型对象
                db_user = UserModel(account=user_info['account'], password=user_info['password'],
                                    name=user_info['name'], age=user_info['age'])
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
        print(user_account)
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
