import requests

def simulate_new_intake():
    """
    Simulates sending a new intake to the webhook.
    """
    url = "http://127.0.0.1:8000/webhook/intake"
    
    # Sample intake data
    intake_data = {
        "patientId": "PRE248509",
        "dateOfInjury": "2025-05-11",
        "referredBy": "Dr. Smith",
        "attorneyId": "ATT12345",
        "insurance": {
            "carrier": "Blue Shield",
            "policyNumber": "BS-778899"
        },
        "studies": [
            {
                "cptCode": "72148",
                "bodyPart": "LUMBAR",
                "contrast": false
            }
        ],
        "notes": "Patient prefers morning appointments",
        "flags": {
            "isLienCase": false,
            "needsTransportation": true
        }
    }

    try:
        response = requests.post(url, json=intake_data)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        print("Webhook sent successfully.")
        print("Response:", response.json())

    except requests.exceptions.RequestException as e:
        print(f"Error sending webhook: {e}")

if __name__ == "__main__":
    simulate_new_intake() 