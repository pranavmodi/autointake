from sqlalchemy.orm import Session
from . import models, schemas

def get_patient_by_radflow_id(db: Session, radflow_patient_id: str):
    return db.query(models.Patient).filter(models.Patient.radflow_patient_id == radflow_patient_id).first()

def create_patient(db: Session, radflow_patient_id: str, patient_name: str = None):
    first_name, last_name = (None, None)
    if patient_name:
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

def create_intake_process(db: Session, patient_id: int, payload: schemas.IntakeWebhookPayload):
    db_intake_process = models.IntakeProcess(
        patient_id=patient_id,
        date_of_injury=payload.date_of_injury,
        referred_by=payload.referred_by,
        attorney_id=payload.attorney_id,
        notes=payload.notes,
        is_lien_case=payload.flags.is_lien_case,
        needs_transportation=payload.flags.needs_transportation
    )
    db.add(db_intake_process)
    db.commit()
    db.refresh(db_intake_process)

    # Create insurance record
    db_insurance = models.Insurance(
        carrier=payload.insurance.carrier,
        policy_number=payload.insurance.policy_number,
        intake_process_id=db_intake_process.id
    )
    db.add(db_insurance)

    # Create study records
    for study in payload.studies:
        db_study = models.Study(
            cpt_code=study.cpt_code,
            body_part=study.body_part,
            contrast=study.contrast,
            intake_process_id=db_intake_process.id
        )
        db.add(db_study)
    
    db.commit()
    db.refresh(db_intake_process)
    return db_intake_process

# === System Settings CRUD ===

def get_setting(db: Session, key: str) -> models.SystemSettings:
    """
    Retrieves a setting from the database by its key.
    """
    return db.query(models.SystemSettings).filter(models.SystemSettings.key == key).first()

def get_is_system_enabled(db: Session) -> bool:
    """
    A specific helper to check if the intake system is enabled.
    Returns True if the setting is 'true', otherwise False.
    """
    setting = get_setting(db, "intake_system_enabled")
    if setting:
        return setting.value.lower() == 'true'
    return False # Default to disabled if not set for safety

def update_setting(db: Session, key: str, value: str) -> models.SystemSettings:
    """
    Updates a setting's value in the database.
    """
    db_setting = get_setting(db, key)
    if db_setting:
        db_setting.value = value
        db.commit()
        db.refresh(db_setting)
    return db_setting
