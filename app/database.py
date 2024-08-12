from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
import os


# Use environment variables for better security
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "fastapi")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")

# Construct the SQLAlchemy URL
DATABASE_URL = URL.create(
    drivername="postgresql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME
)

# if you are using the sqllite database that is ruing in the memory the use have to pass the 
#  connect_args={"check_same_thread": False} as the argument in the create_engine function otherwise it will give the error
# it is not required for the other databases
engine = create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
        
        
#this not needed as we are using the sqlalchemy to connect to the database
# but if you are using raw sql command the we need have use this code

# import psycopg2
# from psycopg2.extras import RealDictCursor

# while True:    
#     try:
#         connection = psycopg2.connect(host='localhost', database='fastapi', 
#                                     user='postgres', password='root@localhost',
#                                     cursor_factory=RealDictCursor)
#         cursor = connection.cursor()
#         print("connected to the database")
#         break

#     except Exception as e:
#         print("Connection to the database failed")
#         print(f"Error: {e}")
#         time.sleep(2)        