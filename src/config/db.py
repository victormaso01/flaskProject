import sqlalchemy as sa
import sqlalchemy.orm as orm


from sqlalchemy.ext.declarative import declarative_base
from src.config.config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(Config.DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
