from db import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import Date
from sqlalchemy.orm import relationship


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    location = Column(String(200), nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(String())
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    collaborator_id = Column(
        Integer,
        ForeignKey("collaborators.id"),
        nullable=False
    )

    # Establish relationship with other models
    collaborator = relationship("Collaborator", back_populates="events")
    contract = relationship("Contract", back_populates="events")
