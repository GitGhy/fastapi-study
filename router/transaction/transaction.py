from fastapi import APIRouter

router = APIRouter(prefix="/transaction",
                   tags=["transaction"],
                   responses={404: {"msg": "交易失败"}}, )


@router.get("/payment")
async def payment():
    return {"msg": "交易成功"}
