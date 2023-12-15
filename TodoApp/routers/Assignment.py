from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field
from datetime import timedelta,datetime
import model
from model import Users
from passlib.context import CryptContext
from typing import Annotated
from sqlalchemy.orm import Session
from database import SessionLocal
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from .auth import get_current_user


router=APIRouter(
prefix="/Users",
    tags=['Users']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency=Annotated[Session,Depends(get_db)]
user_dependency=Annotated[Session,Depends(get_current_user)]
bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')

class UserVerification(BaseModel):
    password:str
    new_password:str=Field(min_legth=6)

@router.get("/user",status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency,db:db_dependency):
    if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401,detail='Authentication Failed')
    user_details=db.query(Users).filter(Users.id==user.get('id')).first()
    return user_details

@router.put("/password",status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency,db:db_dependency,
                    user_verification=UserVerification):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
        user=db.query(Users).filter(Users.id==user.get('id')).first()
    if not bcrypt_context.verify(user_verification.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user.hashed_password=bcrypt_context.hash(user_verification.new_password)
    db.add(user)
    db.commit()

@router.put("/phonenumber,{phone_number}",status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user:user_dependency,db:db_dependency,
                    phone_number:str):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
        user=db.query(Users).filter(Users.id==user.get('id')).first()
        user.phone_number=phone_number
        db.add(user)
        db.commit()