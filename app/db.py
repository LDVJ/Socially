from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import setting

# DB_URL = URL.create( # doesn't work for the alembic creates issues when updating the db but not for engine as  it is creating the obj which engine can handle but alembic can't
#     drivername="postgresql+psycopg",
#     username=setting.DB_USER,
#     password=setting.DB_PWD,   # raw password, no encoding needed
#     host=setting.DB_HOST,
#     port=setting.DB_PORT,
#     database=setting.DB_NAME,
#     query={"sslmode": "require"}
# )
# DB_URL = "postgresql+psycopg://socially_db_user:gzN4jk8w9lr0a4CTS5S1u0OnUB40Vijn@dpg-d6bv48hr0fns73ar1m4g-a.oregon-postgres.render.com/socially_db?sslmode=require"
DB_URL = f"postgresql+psycopg://{setting.DB_USER}:{setting.DB_PWD}@{setting.DB_HOST}/{setting.DB_NAME}?sslmode=require"

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