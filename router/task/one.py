from fastapi import APIRouter

router = APIRouter(prefix="/task",
                   tags=["task"],
                   responses={404: {"description": "Not found"}}, )


@router.get("/one")
async def read_users():
    print("as")
    return [{"username": "g"}, {"username": "?"}]

