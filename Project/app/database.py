import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Determine the database URL based on the environment
if os.getenv("APP_ENV") == "production":
    # Use local database connection
    URL_DATABASE = 'postgresql://postgres:postgres@postgres-db:5432/postgres'
else :
    URL_DATABASE = 'postgresql://postgres:postgres@localhost:5432/feedbacktool'

# Create SQLAlchemy engine and sessionmaker
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base
Base = declarative_base()