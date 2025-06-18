from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    radflow_patient_id = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    phone_number = Column(String)
    
    intake_processes = relationship("IntakeProcess", back_populates="patient")

class IntakeProcess(Base):
    __tablename__ = "intake_processes"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))
    appointment_id = Column(String, unique=True, nullable=False)
    
    status = Column(String, default="new")
    
    lien_completed = Column(Boolean, default=False)
    id_completed = Column(Boolean, default=False)
    prescreen_completed = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    patient = relationship("Patient", back_populates="intake_processes")
