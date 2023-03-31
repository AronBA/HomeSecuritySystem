import vonage

client = vonage.Client(key="", secret="")
sms = vonage.Sms(client=client)


def SendSMS(recipient):
    response = sms.send_message(
        {
            "from": "C.A.S",
            "to": recipient,
            "text": "Hello there from Camera Alert System (C.A.S)",
        }
    )

    if response["messages"][0]["status"] == "0":
        print("Message Details: ", response)
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {response['messages'][0]['error-text']}")


SendSMS("Registered Account Number")