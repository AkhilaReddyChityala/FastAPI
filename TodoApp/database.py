
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_Database="mysql+pymysql://root:Shiva$123@localhost:3306/TodoApps"
engine=create_engine(URL_Database)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()

