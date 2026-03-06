from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
DATABASE_URL = "sqlite:///./pension_assistant.db" #to create a local database file named pension_assistant.db in the current directory
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # connects python and database
SessionLocal = sessionmaker( bind=engine) #temporary database connection (session) for each request
Base = declarative_base() #create databases tables()
 