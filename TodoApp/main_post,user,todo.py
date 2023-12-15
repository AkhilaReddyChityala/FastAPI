from typing import Annotated
from pydantic import BaseModel,Field
from fastapi import FastAPI,HTTPException,status,Depends,Path
import model
from model import Post
from sqlalchemy.orm import Session
from database import engine,SessionLocal
from routers import auth
import pymysql

app=FastAPI()

model.Base.metadata.create_all(bind=engine)

class PostBase(BaseModel):
    title:str=Field(min_length=0,max_length=100)
    description:str=Field(min_length=0,max_length=100)
    priority:int=Field(gt=0,lt=20)
    complete:bool

class UserBase(BaseModel):
    username:str


class TodoRequest(BaseModel):
    title:str=Field(min_length=0,max_length=100)
    description:str=Field(min_length=0,max_length=100)
    priority:int=Field(gt=0,lt=20)
    complete:bool
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]

# @app.post("/Posts/",status_code=status.HTTP_201_CREATED)
# async def create_post(post:PostBase,db:db_dependency):
#     db_post=model.Post(**post.model_dump())
#     db.add(db_post)
#     db.commit()
#
# @app.get("/Posts/{Post_id}",status_code=status.HTTP_200_OK)
# async def read_post(db:db_dependency,id:int=Path(gt=0)):
#         post = db.query(model.Post).filter(model.Post.id == id).first()
#         if post is None:
#             raise HTTPException(status_code=404, detail='User Not Found')
#         return post
#
#
# @app.get("/Posts/",status_code=status.HTTP_200_OK)
# async def read_allpost(db:db_dependency):
#     post=db.query(model.Post)
#     return post.all()
#
#
# #Put Request
# @app.put("/posts/{Post_id}",status_code=status.HTTP_204_NO_CONTENT)
# async def update_posts(id:int,db:db_dependency,post_base:PostBase):
#     post = db.query(model.Post).filter(model.Post.id == id).first()
#     if post is None:
#         raise HTTPException(status_code=404, detail='User Not Found')
#     return post
#
#     post.title=post_base.title
#     post.description=post_base.description
#     post.priority=post_base.priority
#     post.complete=post_base.complete
#
#     db.add(post)
#     db.commit()
#
# @app.delete("/Post/{Post_id}", status_code=status.HTTP_200_OK)
# async def delete_post(id: int,db:db_dependency):
#     db_post=db.query(model.Post).filter(model.Post.id==id).first()
#     if db_post is None:
#         raise HTTPException(status_code=404, detail='User was Not Found')
#     db.delete(db_post)
#     db.commit()
#
# @app.post("/users/",status_code=status.HTTP_201_CREATED)
# async def create_user(user:UserBase,db:db_dependency):
#     db_user=model.User(**user.model_dump())
#     db.add(db_user)
#     db.commit()
#
# @app.get("/users/{user_id}",status_code=status.HTTP_200_OK)
# async def read_user(user_id:int,db:db_dependency):
#     user=db.query(model.User).filter(model.User.id==user_id).first()
#     if user is None:
#         raise HTTPException(status_code=404,detail='User Not Found')
#     return user
#
# @app.get("/Users/",status_code=status.HTTP_200_OK)
# async def read_allusers(db:db_dependency):
#     user=db.query(model.User)
#     return user.all()
#
# @app.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_user(user_id: int,db:db_dependency):
#     db_user=db.query(model.User).filter(model.User.id==user_id).first()
#     if db_user is None:
#         raise HTTPException(status_code=404, detail='User was Not Found')
#     db.delete(db_user)
#     db.commit()
#
@app.post("/Todos/",status_code=status.HTTP_201_CREATED)
async def create_todos(todo_request:TodoRequest,db:db_dependency):
    db_post=model.Todos(**todo_request.model_dump())
    db.add(db_post)
    db.commit()

@app.get("/Todos/{todos_id}",status_code=status.HTTP_200_OK)
async def read_todo(db:db_dependency,todo_id:int=Path(gt=0)):
        Todo = db.query(model.Todos).filter(model.Todos.id == todo_id).first()
        if Todo is None:
            raise HTTPException(status_code=404, detail='User Not Found')
        return Todo


@app.get("/Todos/",status_code=status.HTTP_200_OK)
async def read_alltodos(db:db_dependency):
    Todo=db.query(model.Todos)
    return Todo.all()


#Put Request
@app.put("/Todos/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todos(db:db_dependency,todo_request:TodoRequest,todo_id:int=Path(gt=0)):
    Todo = db.query(model.Todos).filter(model.Todos.id== todo_id).first()
    if Todo is None:
        raise HTTPException(status_code=404, detail='User Not Found')

    Todo.title=todo_request.title
    Todo.description=todo_request.description
    Todo.priority=todo_request.priority
    Todo.complete=todo_request.complete

    db.add(Todo)
    db.commit()

@app.delete("/Todos/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(db:db_dependency,todo_id: int=Path(gt=0)):
    db_todo=db.query(model.Todos).filter(model.Todos.id==todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail='User was Not Found')
    db.delete(db_todo)
    db.commit()
