from db import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)

    # Establish relationship with other models
    collaborators = relationship("Collaborator", back_populates="department")
