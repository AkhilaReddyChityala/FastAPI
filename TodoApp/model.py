from database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey
from sqlalchemy.dialects.mysql import LONGTEXT
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email=Column(String(50),unique=True)
    username = Column(String(50), unique=True)
    first_name=Column(String(100))
    last_name=Column(String(100))
    hashed_password=Column(LONGTEXT)
    is_active=Column(Boolean,default=True)
    role=Column(String(100))
    phone_number=Column(String(100))
#
# class Post(Base):
#     __tablename__ ='posts'
#
#     id=Column(Integer,primary_key=True,index=True)
#     title = Column(String(50))
#     description = Column(String(200))
#     priority = Column(Integer)
#     complete = Column(Boolean, default=False)

class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50))
    description = Column(String(100))
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id=Column(Integer,ForeignKey("users.id"))



