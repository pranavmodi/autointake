from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configure Jinja2 templates
templates = Jinja2Templates(directory="autointake/app/templates")

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
    # --- KILL SWITCH CHECK ---
    if not crud.get_is_system_enabled(db):
        raise HTTPException(
            status_code=503, 
            detail="Service is currently disabled by an administrator."
        )

    # Check if patient exists, if not create one
    patient = crud.get_patient_by_radflow_id(db, radflow_patient_id=payload.patient_id)
    if not patient:
        patient = crud.create_patient(db, radflow_patient_id=payload.patient_id)

    # Create a new intake process
    intake_process = crud.create_intake_process(db, patient_id=patient.id, payload=payload)
    
    # Here you would add logic to trigger the first step of the intake process,
    # for example, sending an SMS with the lien link.
    
    return {"status": "success", "message": "Intake process started", "intake_process_id": intake_process.id}

@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request, db: Session = Depends(get_db)):
    """
    Serves the admin page to control the system kill switch.
    """
    is_enabled = crud.get_is_system_enabled(db)
    return templates.TemplateResponse("admin.html", {"request": request, "is_enabled": is_enabled})

@app.post("/admin/toggle")
async def toggle_system(db: Session = Depends(get_db)):
    """
    Toggles the system kill switch on or off.
    """
    current_status = crud.get_is_system_enabled(db)
    new_status_str = str(not current_status).lower()
    crud.update_setting(db, "intake_system_enabled", new_status_str)
    
    # Redirect back to the admin page to show the updated status
    return RedirectResponse(url="/admin", status_code=303)

@app.get("/")
async def root():
    return {"message": "Welcome to the AutoIntake API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
