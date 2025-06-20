from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime

class InsuranceBase(BaseModel):
    carrier: str
    policy_number: str = Field(alias="policyNumber")

    class Config:
        from_attributes = True
        populate_by_name = True

class StudyBase(BaseModel):
    cpt_code: str = Field(alias="cptCode")
    body_part: str = Field(alias="bodyPart")
    contrast: bool

    class Config:
        from_attributes = True
        populate_by_name = True

class Flags(BaseModel):
    is_lien_case: bool = Field(alias="isLienCase")
    needs_transportation: bool = Field(alias="needsTransportation")

    class Config:
        populate_by_name = True

class PatientBase(BaseModel):
    radflow_patient_id: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None

    class Config:
        from_attributes = True

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int

    class Config:
        from_attributes = True

class IntakeProcessBase(BaseModel):
    appointment_id: Optional[str] = None
    status: Optional[str] = "new"
    lien_completed: Optional[bool] = False
    id_completed: Optional[bool] = False
    prescreen_completed: Optional[bool] = False

    class Config:
        from_attributes = True

class IntakeProcessCreate(IntakeProcessBase):
    pass

class IntakeProcess(IntakeProcessBase):
    id: int
    patient_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class IntakeWebhookPayload(BaseModel):
    patient_id: str = Field(alias="patientId")
    date_of_injury: date = Field(alias="dateOfInjury")
    referred_by: str = Field(alias="referredBy")
    attorney_id: str = Field(alias="attorneyId")
    insurance: InsuranceBase
    studies: List[StudyBase]
    notes: str
    flags: Flags

    class Config:
        populate_by_name = True
