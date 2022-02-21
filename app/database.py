from enum import auto
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'#in my password @ was there and after @ it will take it as server host name. That's why I used quote() to access my password!!!

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base = declarative_base()
#A base class stores a catlog of classes and mapped tables in the Declarative system. 
# This is called as the declarative base class. 
# There will be usually just one instance of this base in a commonly imported module. 
# The declarative_base() function is used to create base class.

def get_db():
    db=SessionLocal()
    try:
        yield db #yield is same like return keyword but it will be like a generator to the function and executes only when interates over generator.
    finally:
        db.close()



# while True:
#     try:
#         connection = psycopg2.connect(host='localhost',database='pdfapi',user='postgres',password='Pr@veen123', cursor_factory=RealDictCursor)
#         cursor = connection.cursor()
#         print("Database successfully connected")
#         break
#     except Exception as error:
#         print("")
#         print("connection failed!!!!!! Error is {}".format(error))
#         time.sleep(5)
