from fastapi import FastAPI
from starlette.responses import JSONResponse
from router.users import user
from router.task import one


# 异常处理
async def exception_not_found(request, exc):
    return JSONResponse({
        "code": exc.status_code,
        "error": exc.detail,
    }, status_code=exc.status_code)


exception_handlers = {
    404: exception_not_found,
}
app = FastAPI(title="FastAPI",
              description="FastAPI文档",
              version="0.0.1",
              exception_handlers=exception_handlers)
app.include_router(user.router)
app.include_router(one.router)


@app.get("/", tags=['Hello World'])
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}", tags=['app实例对象注册接口'])
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app='main:app', host="0.0.0.0", port=8000, reload=True)
