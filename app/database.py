from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

#SQLAlchemy Engin
engine=create_engine(settings.DATABASE_URL,connect_args={"check_same_thread":False})

#Session Factory
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

#Base class for models
Base=declarative_base()


    