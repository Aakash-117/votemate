import random
from twilio.rest import Client

TWILIO_ACCOUNT_SID = "AC0dac83aba700857ba83c91c3555c9d9c"
TWILIO_AUTH_TOKEN = "e6326dd4e439b9cdfe8c550b2794049d"
TWILIO_PHONE_NUMBER = "+91 9063839289" 

def generate_otp():
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))

def send_otp(phone_number):
    """Send OTP to the given phone number using Twilio."""
    otp = generate_otp()
    
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f"Your OTP is: {otp}. Do not share it with anyone.",
        from_=TWILIO_PHONE_NUMBER,
        to=phone_number
    )
    
    print(f"OTP sent successfully to {phone_number}")
    return otp
if __name__ == "__main__":
    user_phone = input("Enter your phone number: ")
    send_otp(user_phone)
