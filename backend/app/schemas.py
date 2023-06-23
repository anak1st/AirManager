from datetime import datetime
from pydantic import BaseModel

# 定义返回数据的模型，和POST请求的模型

class TaskBase(BaseModel):
    title: str
    description: str | None = None
    deadline: datetime

# POST
class TaskCreate(TaskBase):
    pass


# 返回
class Task(TaskBase):
    id: int
    owner_id: int
    is_done: bool
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str

# POST
class UserCreate(UserBase):
    password: str
    name: str

class UserLogin(UserBase):
    password: str


# 返回
class User(UserBase):
    id: int
    name: str
    is_active: bool
    tasks: list[Task] = []

    class Config:
        orm_mode = True
