# Project Implementation Plan: AI-Driven Intake

This document outlines the remaining tasks required to fully implement the AI-driven patient intake and reminder system.

## Phase 1: Core Infrastructure & Setup

- [ ] **Finalize Environment Configuration (`.env`)**
  - [ ] Add `DATABASE_URL` for PostgreSQL.
  - [ ] Add `OPENAI_API_KEY` for Voice AI.
  - [ ] Add `RADFLOW_API_URL` and `RADFLOW_API_TOKEN` for RadFlow 360 integration.
  - [ ] Add `FRONT_API_TOKEN` for human escalation notifications.

- [ ] **Database Model (`autointake/app/models.py`)**
  - [ ] Define the `Intake` table model. It should include fields for:
    - `id` (Primary Key)
    - `patient_id` (from RadFlow)
    - `patient_phone_number`
    - `financial_type` ('PI' or 'Non-PI')
    - `status` (e.g., 'NEW', 'INITIAL_SMS_SENT', 'SMS_REMINDER_SENT', 'VOICE_REMINDER_SENT', 'NEEDS_HUMAN_CALL', 'COMPLETED', 'CANCELED')
    - `last_communication_at` (Timestamp)
    - `created_at` / `updated_at` (Timestamps)
  - [ ] Generate and run a new Alembic migration to apply the schema to the database.

## Phase 2: Service Integrations

- [ ] **RadFlow 360 API Client (`autointake/app/services/radflow_service.py`)**
  - [ ] Create the service file.
  - [ ] Implement `get_patient_document_status(patient_id)`.
    - This function will act as the "MCP Client" you mentioned.
    - It will call the RadFlow "To-Do API" to fetch a list of required documents and their completion status (e.g., `{ "lien_signed": true, "id_uploaded": false, "prescreen_completed": true }`).
  - [ ] Implement any other necessary API calls (e.g., fetching patient details).

- [ ] **AI Voice Service (`autointake/app/services/voice_service.py`)**
  - [ ] Create the service file.
  - [ ] Implement the `make_voice_call(patient_phone_number, message_script)` function.
  - [ ] This function will use the OpenAI Real-Time Voice API to place the automated reminder call.

- [ ] **Human Escalation Service (`autointake/app/services/front_service.py`)**
  - [ ] Create the service file.
  - [ ] Implement a function `notify_intake_coordinator(patient_id)`.
  - [ ] This function will make an API call to Front to create a new task or conversation, assigning it to the "Intake Coordinator Help" channel/tag.

## Phase 3: Application Logic

- [ ] **FastAPI Webhook Endpoint (`autointake/app/main.py`)**
  - [ ] Create a new `/webhooks/radflow/new-order` endpoint.
  - [ ] Add logic to receive and validate the incoming POST request from RadFlow.
  - [ ] Inside the endpoint, create the initial `Intake` record in the database.
  - [ ] Trigger the Celery workflow by calling `start_intake_workflow.delay(...)`.

- [ ] **Flesh out Celery Tasks (`autointake/app/tasks/intake_tasks.py`)**
  - [ ] **`start_intake_workflow`**: No major changes needed, but ensure it correctly logs the start of the process.
  - [ ] **`check_for_reminders_and_escalations`**: This is the core logic.
    - [ ] Remove all placeholder code and comments.
    - [ ] Use `SessionLocal` to create a database session.
    - [ ] Fetch all active intakes from the database.
    - [ ] For each intake, call `radflow_service.get_patient_document_status()`.
    - [ ] If all documents are complete, send the "self-schedule" SMS and update the intake status to `COMPLETED`.
    - [ ] If documents are incomplete, execute the escalation logic using the patient's `status` and `last_communication_at` fields, calling the appropriate services (`send_sms`, `voice_service.make_voice_call`, `front_service.notify_intake_coordinator`).
    - [ ] Ensure the `status` and `last_communication_at` fields are updated after every action.

## Phase 4: Testing & Deployment

- [ ] **Create Evals/Tests (`evals/`)**
  - [ ] Enhance `scenario_1_new_intake.py` to be a full end-to-end test for the happy path.
  - [ ] Create new eval scripts for the 24h, 48h, and 72h escalation scenarios.
- [ ] **Update `README.md`**
  - [ ] Add a section explaining the full architecture and data flow.
  - [ ] Document all required environment variables.
- [ ] **Deployment**
  - [ ] Prepare deployment scripts (e.g., Dockerfile, docker-compose) to run the FastAPI server, Celery worker, and Celery Beat scheduler as separate containers. 