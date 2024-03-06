# 开箱即用的**FastApi**模板

## 1、项目结构


```markdown
|----.cache\                    # Python编译缓存
|    |----v\
|    |    |----cache\
|    |    |    |----lastfailed
|----alembic\                   # 数据库迁移目录
|    |----versions\
|    |    |----0be20312ffea_第一次迁移.py
|    |----env.py
|    |----README
|    |----script.py.mako
|----api\                       # Api路由目录
|    |----users\
|    |    |----user.py
|----db\                        # 数据库目录
|    |----__init__.py
|    |----crud.py               # 数据库操作
|    |----database.py           # 数据库连接
|    |----models.py             # 数据模型
|    |----run.py                # 数据库迁移脚本
|    |----schema.py             # 数据表结构
|----static\                    # 静态文件目录
|    |----css\
|    |----js\
|    |----favicon.png
|----test\                      # 单元测试目录
|    |----__init__.py
|    |----test_users.py
|----utils\                     # 工具/依赖目录
|    |----jwt_token.py          # JWT Token生成与解密工具
|----alembic.ini                # Alembic配置文件
|----app.py                     # 应用启动文件
|----main.py                    # 应用入口文件
|----README.md                  # 项目说明文档
|----requirements.txt           # 项目依赖清单
```

## 2、环境配置

安装依赖

```python
pip install -r requirements.txt
# 使用清华源
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

创建数据库（mysql）

```mysql
# 在终端中进入mysql
mysql -u你的用户名 -p你的密码
例：mysql -uroot -p123456

# 创建数据库
CREATE DATABASE 数据库名字 DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
例：CREATE DATABASE fastapi DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```

迁移数据库（生成表）

```cmd
# 先在终端输入以下命令。"init"这里可以随便写自己的备注
alembic revision --autogenerate -m "init"
# 接着输入
alembic upgrade head
```

## 3、运行

```python
python3 app.py  # 默认端口为8000，可在app.py文件中修改

# 用户注册路由
http://127.0.0.1:8000/user/register
# 用户登陆路由
http://127.0.0.1:8000/user/login
# 验证token路由
http://127.0.0.1:8000/user/token
```

*未完待续......*
