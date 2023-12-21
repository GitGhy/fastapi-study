from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from db.schema import UserModelSchema
from utils.jwt_token import JWTToken
from db.crud import UserModelCrud
from db.database import get_db

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


class UserInfoVerify:
    def __init__(self, request: Request):
        self.request = request

    @staticmethod
    async def userinfo_verify(name: str, age: int):
        """
        验证用户信息是否有效
        """
        if not name or not age:
            return False, {
                "code": 400,
                "success": False,
                "msg": "参数类型为空",
            }
        if not isinstance(name, str) or not isinstance(age, int):
            return False, {
                "code": 401,
                "success": False,
                "msg": "参数类型错误",
            }
        return True, "success"

    @staticmethod
    async def user_verify(account: str, password: str):
        """
        验证用户账号和密码是否有效
        """
        if not account or not password:
            return False, {
                "code": 400,
                "success": False,
                "msg": "参数类型为空",
            }
        if not isinstance(account, str) or not isinstance(password, str):
            return False, {
                "code": 401,
                "success": False,
                "msg": "参数类型错误",
            }
        return True, "success"


@router.post("/register", tags=["注册"])
async def register_user(unv: UserInfoVerify = Depends(), db: AsyncSession = Depends(get_db)):
    get_json = await unv.request.json()
    name = get_json.get('name')
    age = get_json.get('age')
    account = get_json.get('account')
    password = get_json.get('password')
    # 验证用户信息
    is_valid, msg = await unv.user_verify(account, password)
    if not is_valid:
        return HTTPException(status_code=400, detail=msg)
    is_valid, msg = await unv.userinfo_verify(name, age)
    if not is_valid:
        return HTTPException(status_code=400, detail=msg)
    # 验证用户用户信息是否有效
    user_info = UserModelSchema(name=name, age=age, account=account, password=password)
    add_user, msg = await UserModelCrud.create_user(db=db, user=user_info)
    raise HTTPException(status_code=200, detail=msg)


@router.post("/login", tags=["登录"])
async def read_userinfo(unv: UserInfoVerify = Depends(), db: AsyncSession = Depends(get_db)):
    # 获取用户信息
    get_json = await unv.request.json()
    account = get_json.get('account')
    password = get_json.get('password')

    # 验证用户账号和密码
    is_valid, msg = await unv.user_verify(account, password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)

    select_user, user_info = await UserModelCrud.get_user(db=db, user_account=account)
    print("是否存在", select_user, "用户信息", user_info)
    if not select_user:
        raise HTTPException(status_code=400,
                            detail={
                                "code": 400,
                                "success": False,
                                "msg": "用户不存在"
                            })
    if user_info['password'] != password:
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
