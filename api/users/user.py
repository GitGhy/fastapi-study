from db.schema import UserModelSchema, UserLoginSchema
from fastapi import APIRouter, Depends, HTTPException
from werkzeug.security import check_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from utils.jwt_token import JWTToken
from db.crud import UserModelCrud
from db.database import get_db

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", tags=["注册"])
async def register_user(user_info: UserModelSchema, db: AsyncSession = Depends(get_db)):
    add_user, msg = await UserModelCrud.create_user(db=db, user=user_info)
    raise HTTPException(status_code=200, detail=msg)


@router.post("/login", tags=["登录"])
async def read_userinfo(user_login_info: UserLoginSchema, db: AsyncSession = Depends(get_db)):
    # 查询数据库是否存在该用户
    select_user, user_info = await UserModelCrud.get_user(db=db, user_account=user_login_info.account)
    print("是否存在:", select_user, "用户信息:", user_info)
    if not select_user:
        raise HTTPException(status_code=400,
                            detail={
                                "code": 400,
                                "success": False,
                                "msg": "用户不存在"
                            })
    if not check_password_hash(user_info['password'], user_login_info.password):
        raise HTTPException(status_code=500,
                            detail={
                                "code": 400,
                                "success": False,
                                "msg": "密码错误",
                            })
    userinfo = {
        'account': user_info['account'],
        'name': user_info['name'],
        'age': user_info['age']
    }
    # 返回登录成功信息和生成的token
    return_data = {
        "code": 200,
        "success": True,
        "msg": "登录成功",
        "userinfo": userinfo,
        "token": JWTToken.generate_token(userinfo)
    }
    return return_data


@router.get("/token", tags=["验证token"])
async def token(current_user: dict = Depends(JWTToken())):
    # 返回验证成功的信息和用户信息
    return_data = {
        "code": 200,
        "success": True,
        "msg": "验证成功",
        "user_info": current_user
    }
    return return_data
