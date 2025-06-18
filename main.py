from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class Intake(BaseModel):
    patient_id: str
    patient_name: str
    appointment_id: str
    status: str
    document_urls: Optional[list[str]] = None

@app.post("/webhook/intake")
async def receive_intake(intake: Intake):
    """
    Webhook to receive intake information.
    """
    print(f"Received intake information: {intake.model_dump_json(indent=2)}")
    # Here you would add logic to process the intake information,
    # for example, updating a database or triggering another process.
    return {"status": "success", "message": "Intake received"}

@app.get("/")
async def root():
    return {"message": "Welcome to the AutoIntake API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
