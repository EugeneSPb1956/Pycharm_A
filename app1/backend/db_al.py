from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
# from sqlalchemy import Column, Integer, String, Boolean

# engine = create_engine('sqlite:///db_al.sqlite3', echo=True)
engine = create_engine('sqlite:///db_al.db', echo=True)

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

