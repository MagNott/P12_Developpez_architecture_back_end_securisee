from db import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Status(BaseModel):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), unique=True, nullable=False)

    # Establish relationship with other models
    contracts = relationship("Contract", back_populates="status")
