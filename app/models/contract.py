from db import Base
from sqlalchemy import Column, Float, ForeignKey, Integer
from sqlalchemy import Date
from sqlalchemy.orm import relationship


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    contract_amount = Column(Float, nullable=False)
    amount_due = Column(Float, nullable=False)
    creation_date = Column(Date, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    status_id = Column(Integer, ForeignKey("statuses.id"), nullable=False)

    # Establish relationship with other models
    customer = relationship("Customer", back_populates="contracts")
    status = relationship("Status", back_populates="contracts")
    events = relationship("Event", back_populates="contract")
