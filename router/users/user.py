from fastapi import APIRouter

router = APIRouter(prefix="/user",
                   tags=["user"],
                   responses={404: {"description": "Not found"}}, )


@router.get("/{name}")
async def read_users(name: str):
    return [{"username": name}]
