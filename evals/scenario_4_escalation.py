import requests
import os
from dotenv import load_dotenv

load_dotenv()

def simulate_intake_escalation():
    """
    Scenario: Patient abandons the intake process midway.

    Expected Behavior:
    The system should track the patient's progress. If the patient signs the
    lien but does not proceed to the next step after a set time, escalation
    protocols are initiated.

    - After 48 hours: An automated AI voice call is made to the patient,
      prompting them to check their SMS messages to continue the intake process.
    - After 72 hours: If still incomplete, the task is flagged for a human
      intake coordinator to call the patient directly.
    """
    port = os.getenv("PORT", "8000")
    url = f"http://127.0.0.1:{port}/webhook/intake"
    
    intake_data = {
        "patientId": "PRE248512",
        "dateOfInjury": "2025-05-15",
        "referredBy": "Dr. Davis",
        "attorneyId": "ATT45678",
        "insurance": {
            "carrier": "United Healthcare",
            "policyNumber": "UH-789012"
        },
        "studies": [
            {
                "cptCode": "72141",
                "bodyPart": "CERVICAL",
                "contrast": False
            }
        ],
        "notes": "Patient has questions about the procedure.",
        "flags": {
            "isLienCase": True,
            "needsTransportation": True
        },
        "intake_process": {
            "lien_signed": True,  # Patient completed step 1
            "id_uploaded": False, # But abandoned before step 2
            "prescreen_completed": False
        }
    }

    try:
        response = requests.post(url, json=intake_data)
        response.raise_for_status()
        
        print("Webhook for 'Intake Escalation' scenario sent successfully.")
        print("Response:", response.json())

    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook for 'Intake Escalation' scenario: {e}")

if __name__ == "__main__":
    simulate_intake_escalation() 