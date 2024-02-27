# **FastApi** templates out of the box

## 1、project structure


```markdown
|----.cache\                    # Python compile cache
|    |----v\
|    |    |----cache\
|    |    |    |----lastfailed
|----alembic\                   # Database Migration Directory
|    |----versions\
|    |    |----0be20312ffea_First migration.py
|    |----env.py
|    |----README
|    |----script.py.mako
|----api\                       # Api routing directory
|    |----users\
|    |    |----user.py
|----db\                        # database directory
|    |----__init__.py
|    |----crud.py               # database operations
|    |----database.py           # Database Connection
|    |----models.py             # Data model
|    |----run.py                # Database migration script
|    |----schema.py             # Data Table Structure
|----static\                    # Static file directory
|    |----css\
|    |----js\
|    |----favicon.png
|----test\                      # Unit Test Catalog
|    |----__init__.py
|    |----test_users.py
|----utils\                     # Tools/Dependency Catalog
|    |----jwt_token.py          # JWT Token Generation and Decryption Tools
|----alembic.ini                # Alembic configuration file
|----app.py                     # Application startup file
|----main.py                    # Application entry file
|----README.md                  # Project Description Document
|----requirements.txt           # Project Dependency List
```

## 2、environment configuration

installation dependency

```python
pip install -r requirements.txt
```

create database（mysql）

```mysql
# Enter in the terminal mysql
mysql -uyou_name -pyou_password
例：mysql -uroot -p123456

# Creating database
CREATE DATABASE database_name DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
例：CREATE DATABASE fastapi DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```

migration database（generation table）

```cmd
# First, enter the following command on the terminal. You can write your own notes here for "init"
alembic revision --autogenerate -m "init"
# Continue to input
alembic upgrade head
```

## 3、run

```python
python3 app.py  # The default port is 8000, which can be modified in the app.py file

# User Registration Routing
http://127.0.0.1:8000/user/register
# User login routing
http://127.0.0.1:8000/user/login
# Verify token routing
http://127.0.0.1:8000/user/token
```

*to be continued......*