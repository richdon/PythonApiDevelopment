from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLAlCHEMY_DATABASE_URL = f'postgresql://' \
                          f'{settings.database_username}:{settings.database_password}@{settings.database_hostname}:' \
                          f'{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLAlCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Tables will extend this class
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
