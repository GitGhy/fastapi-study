from fastapi.routing import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.responses import JSONResponse
from pydantic_settings import BaseSettings
from fastapi import FastAPI
from api.users import user
import traceback


# 定义包含ORM模式设置的Settings类
class Settings(BaseSettings):
    orm_mode: bool = True


# 实例化Settings类为settings对象
settings = Settings()
# 创建FastAPI应用程序实例
app = FastAPI(title="FastAPI",
              description="FastAPI文档",
              version="0.0.1")
# 添加中间件
# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源
    allow_credentials=True,  # 允许证书
    allow_methods=["*"],  # 允许所有请求方法
    allow_headers=["*"],  # 允许所有请求头
    expose_headers=["*"],  # 允许暴露所有头
    max_age=600  # 请求的缓存时间
)
# 压缩数据
app.add_middleware(
    GZipMiddleware,
    minimum_size=1024,  # 压缩大于1024字节的数据
)


# 异常处理器，处理所有异常并返回相应的JSON响应
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


# 处理请求参数验证异常并返回JSON响应
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


# 注册用户路由
app.include_router(user.router)


# 根路由
@app.get("/", tags=['Hello World'])
async def root():
    return {"message": "Hello World"}
