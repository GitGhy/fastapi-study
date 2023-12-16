from fastapi import APIRouter, Depends, Request, HTTPException


router = APIRouter(prefix="/user",
                   tags=["user"],
                   responses={404: {"description": "Not found"}}, )


class Req:
    def __init__(self, request: Request):
        self.request = request


class UserInfoVerify:
    def __init__(self, request: Request):
        self.request = request

    @staticmethod
    async def verification(name: str, age: int):
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


@router.post("/userinfo")
async def read_userinfo(unv: UserInfoVerify = Depends()):
    userinfo = await unv.request.json()
    print(userinfo)
    name = userinfo.get('name')
    age = userinfo.get('age')
    is_valid, msg = await unv.verification(name, age)
    if not is_valid:
        raise HTTPException(status_code=400, detail=msg)
    return_data = [{
        "userinfo": {
            'name': userinfo['name'],
            'age': userinfo['age']
        }
    }]
    return return_data
