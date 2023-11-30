from fastapi import APIRouter

router = APIRouter(prefix="/login",
                   tags=["login"],
                   responses={500: {"msg": "登录失败"}}, )


@router.get("/password")
async def password_login():
    """
    密码登录
    :return:
    """

    return {
        "msg":"登录成功"
    }
