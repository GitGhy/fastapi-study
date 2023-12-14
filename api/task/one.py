from fastapi import APIRouter

router = APIRouter(prefix="/task",
                   tags=["task"],
                   responses={404: {"description": "Not found"}}, )


@router.get("/one")
async def read_users():
    print("as")
    print("cs")
    print("网易")
    print("知乎")
    return [{"username": "g"}, {"username": "?"}]


@router.post("/two")
async def read_users():
    return {"method": "post"}
