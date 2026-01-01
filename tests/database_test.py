from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base 
from models.user import User
from models.case import Case


TEST_DB_URL = "postgresql://postgres:1111@localhost:5432/database_test"

engine = create_engine(TEST_DB_URL, echo=False)
SessionTest = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_test_session():
    session = SessionTest()
    try:
        yield session
    finally:
        session.commit()
        session.close()

def init_test_db():
    Base.metadata.create_all(bind=engine)

def drop_test_db():
    Base.metadata.drop_all(bind=engine)
