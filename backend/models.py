from sqlalchemy import Column, Integer, String
from database import Base


class SortMaps(Base):
    __tablename__ = "sortmaps"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    value = Column(String, unique=False, index=True)
