from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/webhook/intake", status_code=201)
async def receive_intake(payload: schemas.IntakeWebhookPayload, db: Session = Depends(get_db)):
    """
    Webhook to receive intake information.
    """
    # Check if patient exists, if not create one
    patient = crud.get_patient_by_radflow_id(db, radflow_patient_id=payload.patient_id)
    if not patient:
        patient = crud.create_patient(db, radflow_patient_id=payload.patient_id, patient_name=payload.patient_name)

    # Create a new intake process
    intake_process = crud.create_intake_process(db, appointment_id=payload.appointment_id, patient_id=patient.id)
    
    # Here you would add logic to trigger the first step of the intake process,
    # for example, sending an SMS with the lien link.
    
    return {"status": "success", "message": "Intake process started", "intake_process_id": intake_process.id}

@app.get("/")
async def root():
    return {"message": "Welcome to the AutoIntake API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
