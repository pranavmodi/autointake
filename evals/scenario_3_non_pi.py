import requests
import os
from dotenv import load_dotenv

load_dotenv()

def simulate_intake_non_pi():
    """
    Scenario: New intake for a Non-Personal Injury case.

    Expected Behavior:
    For Non-PI cases, the lien signing process is skipped. The system should
    initiate a 2-step intake process, requesting only the Photo ID and the
    Pre-screen form.
    """
    port = os.getenv("PORT", "8000")
    url = f"http://127.0.0.1:{port}/webhook/intake"
    
    intake_data = {
        "patientId": "PRE248511",
        "dateOfInjury": None,  # No DOI for non-pi
        "referredBy": "Dr. Miller",
        "attorneyId": None, # No attorney for non-pi
        "insurance": {
            "carrier": "Cigna",
            "policyNumber": "CI-445566"
        },
        "studies": [
            {
                "cptCode": "70553",
                "bodyPart": "BRAIN",
                "contrast": True
            }
        ],
        "notes": "Patient needs evening appointment.",
        "flags": {
            "isLienCase": False,
            "needsTransportation": False
        },
        "intake_process": {
            "lien_signed": None, # Lien is not applicable
            "id_uploaded": False,
            "prescreen_completed": False
        }
    }

    try:
        response = requests.post(url, json=intake_data)
        response.raise_for_status()
        
        print("Webhook for 'Non-PI Intake' scenario sent successfully.")
        print("Response:", response.json())

    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook for 'Non-PI Intake' scenario: {e}")

if __name__ == "__main__":
    simulate_intake_non_pi() 