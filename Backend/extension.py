from twilio.rest import Client
from disease_detection import predict

def send_sms(account_sid,auth_token,twilio_phone_number,user_phone_number, message):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=message,
        from_=twilio_phone_number,
        to=user_phone_number
    )
    return message.sid

def predict_and_notify(file_path):
    result = predict(file_path)
    print(result)
    # Check if the predicted class is not healthy
    if result['class'] not in ['Potato___healthy', 'Tomato_healthy', 'Pepper__bell___healthy']:
        message = f"Alert: Unhealthy plant detected - Class: {result['class']}, Confidence: {result['confidence']}"
        send_sms(message)
        print("SMS Sent!")
    else:
        print("No action needed.")

if __name__ == "__main__":
    image_file_path = "potato_exl.jpeg"  
    predict_and_notify(image_file_path) 

