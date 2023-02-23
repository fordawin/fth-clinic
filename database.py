from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# SQLALCHEMY_DATABASE_URL = os.environ.get('DB_URL')

# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/fth-db"
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/clinicdb"
# SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root@localhost/clinicdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except:
        db.close()