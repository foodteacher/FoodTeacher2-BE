from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase

from typing import Generator

from FT_api.core.config import get_setting


settings = get_setting()

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://{}:{}@{}:{}/{}".format(
    settings.MYSQL_USER,
    settings.MYSQL_PASSWORD,
    settings.MYSQL_HOST,
    settings.MYSQL_PORT,
    settings.MYSQL_DATABASE,
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    pool_pre_ping=True,
    max_overflow=150,
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
insp = inspect(engine)

# Base = declarative_base()
class Base(DeclarativeBase):
    pass

def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()