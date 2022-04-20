from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

f = open('app/files/pw.txt', 'r')
pw = f.read()
f.close()

SQLAlCHEMY_DATABASE_URL = f'postgresql://postgres:{pw}@localhost/fast-api-social-media-app'

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
