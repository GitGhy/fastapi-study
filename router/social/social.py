from fastapi import APIRouter

router = APIRouter(prefix="/social",
                   tags=["social"],
                   responses={500: {"msg": "系统错误"}}, )


@router.get("/social")
async def social():
    return {"msg": "发送成功"}
