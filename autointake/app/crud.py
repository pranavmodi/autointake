from sqlalchemy.orm import Session
from . import models, schemas

def get_patient_by_radflow_id(db: Session, radflow_patient_id: str):
    return db.query(models.Patient).filter(models.Patient.radflow_patient_id == radflow_patient_id).first()

def create_patient(db: Session, radflow_patient_id: str, patient_name: str):
    first_name, last_name = patient_name.split(" ", 1) if " " in patient_name else (patient_name, "")
    db_patient = models.Patient(
        radflow_patient_id=radflow_patient_id,
        first_name=first_name,
        last_name=last_name
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def create_intake_process(db: Session, appointment_id: str, patient_id: int):
    db_intake_process = models.IntakeProcess(
        appointment_id=appointment_id,
        patient_id=patient_id
    )
    db.add(db_intake_process)
    db.commit()
    db.refresh(db_intake_process)
    return db_intake_process
