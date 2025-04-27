from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# an Engine, which the Session will use for connection
# resources
# SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip_address/host_name>/<database_name>")

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL) # establishing connection
SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind = engine) # talk to sql database # autoflush automatically push the pending changes before commiting

Base = declarative_base()

# gets a session for a query using api endpoint, when the queery is finished, it closes the session
def get_db():
    db = SessionLocal()
    try:
        yield db # yield, pauses, returns and then continues from the next line
    finally: # ensures that the code will run no matter what
        db.close()
      
# # Psycopg2 server connection
# while True:    
#     try:
#         conn = psycopg2.connect(host = 'localhost', database ='fastapi', # the database name should be same as the database you created
#                                 user = 'postgres', password = '240701', # user and password
#                                 cursor_factory= RealDictCursor) # sets up the column names
#         cursor = conn.cursor() # cursor, check psycopg2 documentation
#         print('Successfully connected to the database!')
#         break
#     except Exception as error:
#         print('Connection to database failed!')
#         print(f'Error: {error}')
#         time.sleep(2) # keep on trying until connection is successful