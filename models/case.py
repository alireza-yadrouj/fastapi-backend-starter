from sqlalchemy import Column, Integer, String
from .base import Base

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    owner_username = Column(String, nullable=False)
