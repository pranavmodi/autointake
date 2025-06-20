import os
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

def send_sms(to: str, body: str):
    """
    Sends an SMS message to a specified phone number using Twilio.

    Args:
        to (str): The recipient's phone number in E.164 format.
        body (str): The content of the SMS message.
    
    Returns:
        str: The message SID if successful, otherwise an error message.
    """
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")
    twilio_number = os.getenv("TWILIO_ADMIN_NUMBER")

    if not all([account_sid, auth_token, twilio_number]):
        return "Error: Twilio environment variables not set."

    try:
        client = Client(account_sid, auth_token)
        message = client.messages.create(
            to=to,
            from_=twilio_number,
            body=body
        )
        return message.sid
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    # Example usage:
    # Make sure to set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_ADMIN_NUMBER in your .env file
    # And replace "+15551234567" with a real phone number.
    test_to_number = "+15551234567" 
    message_sid = send_sms(test_to_number, "Hello from the Autointake system!")
    print(f"Message sent with SID: {message_sid}") 