from app.models.user import User
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy import Date


class Customer(User):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    company_name = Column(String(100), nullable=False)
    creation_date = Column(Date)
    last_update = Column(Date)
    commercial_id = Column(
        Integer,
        ForeignKey("collaborators.id"),
        nullable=False
    )

    # Establish relationship with other models
    collaborator = relationship("Collaborator", back_populates="customers")
    contracts = relationship("Contract", back_populates="customer")
