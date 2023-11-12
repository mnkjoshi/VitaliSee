import os
from twilio.rest import Client

account_sid = ""
auth_token = ""
client = Client(account_sid, auth_token)

def send_sms(givenMessage):
    message = client.messages.create(
        body= givenMessage,
        from_= '+16612623969',
        to= '+17802247327'
    )
    return message.sid

def notify_all(result):
    print(result)
    # Check if the predicted class is not healthy
    if result['class'] not in ['Potato___healthy', 'Tomato_healthy', 'Pepper__bell___healthy']:
        message = f"Alert: Unhealthy plant detected - Class: {result['class']}, Confidence: {result['confidence']}"
        send_sms(message)
        print("SMS Sent!")
    else:
        print("No action needed.")
