import requests
import os
from dotenv import load_dotenv

load_dotenv()

def simulate_intake_all_docs_complete():
    """
    Scenario: New intake for a patient with all documents already completed.

    Expected Behavior:
    The system should detect that all required documents (Lien, Photo ID, Pre-screen)
    are already on file. It should send a single SMS to the patient with a direct link
    to schedule their appointment, bypassing the multi-step intake process.

    SMS Template:
    "Hi [Patient First Name], we received a new imaging order from your doctor.
    Since your intake is already complete (thanks for that!), you can schedule
    your appointment online here: :arrow_right: [Scheduling Link] or call us at
    818-629-1169 (Mon-Fri, 8 AM – 5 PM). We're happy to assist you!"
    """
    port = os.getenv("PORT", "8000")
    url = f"http://127.0.0.1:{port}/webhook/intake"
    
    intake_data = {
        "patientId": "PRE248510",
        "dateOfInjury": "2025-05-12",
        "referredBy": "Dr. Jones",
        "attorneyId": "ATT67890",
        "insurance": {
            "carrier": "Aetna",
            "policyNumber": "AE-112233"
        },
        "studies": [
            {
                "cptCode": "73721",
                "bodyPart": "KNEE",
                "contrast": True
            }
        ],
        "notes": "Patient is claustrophobic.",
        "flags": {
            "isLienCase": True,
            "needsTransportation": False
        },
        # Flags indicating all documents are already on file
        "intake_process": {
            "lien_signed": True,
            "id_uploaded": True,
            "prescreen_completed": True
        }
    }

    try:
        response = requests.post(url, json=intake_data)
        response.raise_for_status()
        
        print("Webhook for 'All Docs Complete' scenario sent successfully.")
        print("Response:", response.json())

    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook for 'All Docs Complete' scenario: {e}")

if __name__ == "__main__":
    simulate_intake_all_docs_complete() 