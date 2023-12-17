from fastapi import APIRouter, Depends, Request, HTTPException
from utils.jwt_token import JWTToken

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
    async def user_verify(account: int, password: str):
        """
        验证用户账号和密码是否有效
        """
        if not account or not password:
            return False, {
                "code": 400,
                "success": False,
                "msg": "参数类型为空",
            }
        if not isinstance(account, int) or not isinstance(password, str):
            return False, {
                "code": 401,
                "success": False,
                "msg": "参数类型错误",
            }
        return True, "success"


@router.post("/login", tags=["生成token"])
async def read_userinfo(unv: UserInfoVerify = Depends()):
    """
    处理用户登录请求
    """
    get_json = await unv.request.json()
    name = get_json.get('name')
    age = get_json.get('age')
    account = get_json.get('account')
    password = get_json.get('password')

    # 验证用户信息
    is_valid, msg = await unv.userinfo_verify(name, age)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)

    # 验证用户账号和密码
    is_valid, msg = await unv.user_verify(account, password)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)

    userinfo = {
        'name': name,
        'age': age,
        'account': account,
        'password': password
    }

    # 返回登录成功信息和生成的token
    return_data = {
        "code": 200,
        "success": True,
        "msg": "登录成功",
        "userinfo": get_json,
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
