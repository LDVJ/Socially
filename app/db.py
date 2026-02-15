from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import setting

DB_URL = URL.create(
    drivername="postgresql+psycopg",
    username=setting.DB_USER,
    password=setting.DB_PWD,   # raw password, no encoding needed
    host=setting.DB_HOST,
    port=setting.DB_PORT,
    database=setting.DB_NAME,
)
engine = create_engine(DB_URL)

sessionLocal = sessionmaker(
    autoflush=False,
    autocommit = False,
    bind=engine
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = sessionLocal()
    try:
        print("DB Connected")
        yield db
    finally:
        print("DB Disconnected")
        db.close()