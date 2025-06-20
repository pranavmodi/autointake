import os
import logging
from datetime import datetime, timedelta
from autointake.app.celery_app import celery_app
from autointake.app.services.sms_service import send_sms
from autointake.app.database import SessionLocal
from autointake.app.crud import get_is_system_enabled
# from autointake.app.models import Intake  # Assuming you have an Intake model

# Placeholder for a voice call service
def make_voice_call(patient_phone_number, message):
    logging.info(f"Initiating voice call to {patient_phone_number} with message: '{message}'")
    # In a real implementation, this would call the OpenAI Voice API
    pass

@celery_app.task
def start_intake_workflow(patient_id: int, patient_phone_number: str):
    """
    Kicks off the intake process for a new patient.
    """
    logging.info(f"Starting intake workflow for patient ID: {patient_id}")
    # This would be the template for the initial, all-in-one SMS
    message_body = (
        ":wave: Hi, before we can schedule your appointment, we need you to complete a few quick steps. "
        "Go here to sign your lien, upload your photo ID, and fill out a short screening form: [Patient Portal Link]"
    )
    send_sms(to=patient_phone_number, body=message_body)
    # Here you would update the patient's state in the database
    # db = SessionLocal()
    # intake = db.query(Intake).filter(Intake.id == patient_id).first()
    # intake.status = "INITIAL_SMS_SENT"
    # intake.last_communication_at = datetime.utcnow()
    # db.commit()
    # db.close()

@celery_app.task
def check_for_reminders_and_escalations():
    """
    A periodic task run by Celery Beat to check on the status of all active intakes.
    It runs every 5 minutes.
    """
    db = SessionLocal()
    # --- KILL SWITCH CHECK ---
    if not get_is_system_enabled(db):
        logging.warning("System is disabled. Skipping reminder check.")
        db.close()
        return

    logging.info("Running periodic check for intake reminders and escalations...")

    # Get timing configurations from environment variables, in minutes.
    # Defaults are: 24h for SMS, 48h for voice, 72h for human.
    reminder_delay_mins = int(os.getenv("INTAKE_REMINDER_DELAY_MINS", 24 * 60))
    voice_escalation_mins = int(os.getenv("INTAKE_VOICE_ESCALATION_MINS", 48 * 60))
    # NOTE: The env var name ends in _HOURS, but the value is expected in minutes (e.g., 4320 for 72h)
    human_escalation_mins = int(os.getenv("INTAKE_HUMAN_ESCALATION_HOURS", 72 * 60))

    # --- Database logic would go here ---
    # The following is a conceptual example of what the logic would look like.

    # active_intakes = db.query(Intake).filter(Intake.status != "COMPLETED").all()
    active_intakes = []  # Placeholder

    for intake in active_intakes:
        now = datetime.utcnow()
        last_comm_time = intake.last_communication_at
        mins_since_last_comm = (now - last_comm_time).total_seconds() / 60

        # The logic checks thresholds in descending order of time.
        # Since the task runs every 5 minutes, we check a 5-minute window
        # to ensure the action triggers only once.
        if human_escalation_mins <= mins_since_last_comm < (human_escalation_mins + 5):
            logging.info(f"Escalating patient {intake.patient_id} to human call.")
            # Trigger human call

        elif voice_escalation_mins <= mins_since_last_comm < (voice_escalation_mins + 5):
            logging.info(f"Escalating patient {intake.patient_id} to AI voice call.")
            make_voice_call(intake.patient_phone_number, "Hello, this is a reminder from Precise Imaging...")
            # Update intake status in DB

        elif reminder_delay_mins <= mins_since_last_comm < (reminder_delay_mins + 5):
            logging.info(f"Sending reminder SMS to patient {intake.patient_id}.")
            send_sms(to=intake.patient_phone_number, body="This is a reminder to complete your intake forms.")
            # Update intake status in DB

    db.close() 