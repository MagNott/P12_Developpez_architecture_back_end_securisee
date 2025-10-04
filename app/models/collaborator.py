from app.models.user import User
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class Collaborator(User):
    __tablename__ = "collaborators"

    id = Column(Integer, primary_key=True)
    login = Column(String(20), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )

    # Establish relationship with Department
    department = relationship("Department", back_populates="collaborators")
    customers = relationship("Customer", back_populates="collaborator")
    events = relationship("Event", back_populates="collaborator")
