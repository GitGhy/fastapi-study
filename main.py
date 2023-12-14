import traceback
from fastapi import FastAPI
from starlette.responses import JSONResponse
from fastapi.routing import RequestValidationError
from api.users import user
from api.task import one
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="FastAPI",
              description="FastAPI文档",
              version="0.0.1")

# 添加 CORS 中间件以允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def exception_handler(request, exc):
    response = {
        'code': exc.status_code if hasattr(exc, 'status_code') else 500,
        'success': False,
        'method': request.method,
        'path': request.url.path,
        'error': '服务器内部错误',
        'error_type': exc.__class__.__name__,
        'traceback': traceback.format_exc().splitlines(),
        'exc_info': exc.errors(),
    }
    return JSONResponse(content=response, status_code=500)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    response = {
        'code': exc.status_code if hasattr(exc, 'status_code') else 400,
        'success': False,
        'method': request.method,
        'path': request.url.path,
        'error': '请求参数验证失败',
        'error_type': exc.__class__.__name__,
        'traceback': traceback.format_exc().splitlines(),
        'exc_info': exc.errors()
    }
    return JSONResponse(content=response, status_code=400)


app.include_router(user.router)
app.include_router(one.router)


@app.get("/", tags=['Hello World'])
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}", tags=['app实例对象注册接口'])
async def say_hello(name: int):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app='main:app', host="0.0.0.0", port=8000, reload=True)
