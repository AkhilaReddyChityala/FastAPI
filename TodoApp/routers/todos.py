from typing import Annotated
from pydantic import BaseModel,Field
from fastapi import APIRouter,HTTPException,status,Depends,Path
from sqlalchemy.orm import Session
from database import SessionLocal
import model
from model import Todos
from .auth import get_current_user


router=APIRouter()

class TodoRequest(BaseModel):
    title:str=Field(min_length=0,max_length=100)
    description:str=Field(min_length=0,max_length=100)
    priority:int=Field(gt=0,lt=20)
    complete:bool


class UserBase(BaseModel):
    email:str
    username:str
    first_name:str
    last_name:str
    hashed_password:str
    is_active:bool
    role:str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[Session,Depends(get_current_user)]

# @router.post("/Users/",status_code=status.HTTP_201_CREATED)
# async def create_user(user:UserBase,db:db_dependency):
#     db_user=model.Users(**user.model_dump())
#     db.add(db_user)
#     db.commit()

@router.post("/Todos/",status_code=status.HTTP_201_CREATED)
async def create_todos(user:user_dependency,db:db_dependency,todo_request:TodoRequest):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    db_post=Todos(**todo_request.model_dump(),owner_id=user.get('id'))
    db.add(db_post)
    db.commit()

@router.get("/Todos/{todos_id}",status_code=status.HTTP_200_OK)
async def read_todo(user:user_dependency,db:db_dependency,todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    Todo = db.query(Todos).filter(Todos.id == todo_id)\
                .filter(Todos.owner_id==user.get('id')).first()
    if Todo is not None:
        raise HTTPException(status_code=404, detail='User Not Found')


@router.get("/Todos/",status_code=status.HTTP_200_OK)
async def read_alltodos(user:user_dependency,db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    Todo=db.query(Todos).filter(Todos.owner_id==user.get('id'))
    return Todo.all()


#Put Request
@router.put("/Todos/{todo_id}",status_code=status.HTTP_204_NO_CONTENT)
async def update_todos(user:user_dependency,db:db_dependency,todo_request:TodoRequest,todo_id:int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    Todo = db.query(Todos).filter(Todos.id== todo_id)\
            .filter(Todos.owner_id==user.get('id')).first()
    if Todo is None:
        raise HTTPException(status_code=404, detail='User Not Found')

    Todo.title=todo_request.title
    Todo.description=todo_request.description
    Todo.priority=todo_request.priority
    Todo.complete=todo_request.complete

    db.add(Todo)
    db.commit()

@router.delete("/Todos/{todo_id}", status_code=status.HTTP_200_OK)
async def delete_todo(user:user_dependency,db:db_dependency,todo_id: int=Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    db_todo=db.query(Todos).filter(Todos.id==todo_id)\
        .filter(Todos.owner_id==user.get('id')).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail='User was Not Found')
    db.query(Todos).filter(Todos.id == todo_id) \
        .filter(Todos.owner_id == user.get('id')).delete()
    db.commit()
