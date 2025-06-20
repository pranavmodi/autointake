from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey, Date, Text
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
    appointment_id = Column(String, unique=True, nullable=True)
    
    status = Column(String, default="new")
    
    date_of_injury = Column(Date)
    referred_by = Column(String)
    attorney_id = Column(String)
    notes = Column(Text)
    is_lien_case = Column(Boolean)
    needs_transportation = Column(Boolean)
    
    lien_completed = Column(Boolean, default=False)
    id_completed = Column(Boolean, default=False)
    prescreen_completed = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    patient = relationship("Patient", back_populates="intake_processes")
    insurance = relationship("Insurance", back_populates="intake_process", uselist=False)
    studies = relationship("Study", back_populates="intake_process")

class Insurance(Base):
    __tablename__ = "insurances"

    id = Column(Integer, primary_key=True, index=True)
    carrier = Column(String, nullable=False)
    policy_number = Column(String, nullable=False)
    intake_process_id = Column(Integer, ForeignKey("intake_processes.id"))

    intake_process = relationship("IntakeProcess", back_populates="insurance")

class Study(Base):
    __tablename__ = "studies"

    id = Column(Integer, primary_key=True, index=True)
    cpt_code = Column(String, nullable=False)
    body_part = Column(String, nullable=False)
    contrast = Column(Boolean, default=False)
    intake_process_id = Column(Integer, ForeignKey("intake_processes.id"))

    intake_process = relationship("IntakeProcess", back_populates="studies")
