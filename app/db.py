from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import setting

DB_URL = f'postgresql+psycopg://{setting.DB_USER}:{setting.DB_PWD}@{setting.DB_HOST}:{setting.DB_PORT}/{setting.DB_NAME}'

engine = create_engine(DB_URL)

sessionLocal = sessionmaker(
    autoflush=False,
    autocommit = False,
    bind=engine
)

Base = DeclarativeBase()

def get_db():
    db = sessionLocal()
    try:
        print("DB Connected")
        yield db
    finally:
        print("DB Disconnected")
        db.close()