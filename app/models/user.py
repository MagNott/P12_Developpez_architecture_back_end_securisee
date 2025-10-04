from db import Base
from sqlalchemy import Column, String


class User(Base):
    __abstract__ = True  # This class won't be mapped to a table

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    mail = Column(String, unique=True, nullable=False)
    phone_number = Column(String(15), nullable=False)
