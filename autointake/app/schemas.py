from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class PatientBase(BaseModel):
    radflow_patient_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int

    class Config:
        orm_mode = True

class IntakeProcessBase(BaseModel):
    appointment_id: str
    status: Optional[str] = "new"
    lien_completed: Optional[bool] = False
    id_completed: Optional[bool] = False
    prescreen_completed: Optional[bool] = False

class IntakeProcessCreate(IntakeProcessBase):
    pass

class IntakeProcess(IntakeProcessBase):
    id: int
    patient_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class IntakeWebhookPayload(BaseModel):
    patient_id: str
    patient_name: str
    appointment_id: str
    status: str
    document_urls: Optional[List[str]] = None
