from twilio.rest import Client

def send_whatsapp_message(phone_number, message_body):
    account_sid = 'ACf9e003694c14701c5508f0b8856599bf'  # Replace with your Twilio SID
    auth_token = '1708c9857c5914f38fb1df010021cf10'    # Replace with your Twilio Auth Token
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',  # Your Twilio WhatsApp sandbox number
        body=message_body,
        to=f'whatsapp:{phone_number}'
    )
    return message.sid
