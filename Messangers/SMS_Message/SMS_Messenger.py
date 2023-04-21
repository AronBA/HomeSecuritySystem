import vonage

client = vonage.Client(key="", secret="")
sms = vonage.Sms(client=client)


def sendSMS(recipient, cameraNum: int, msg):
    response = sms.send_message(
        {
            "from": "C.A.S",
            "to": recipient,
            "text": f"""
********************************
Motion detected by Camera #{cameraNum}
********************************
{msg}
""",
        }
    )

    if response["messages"][0]["status"] == "0":
        print("Message Details: ", response)
        print("Message sent successfully.")
    else:
        print(f"Message failed with error: {response['messages'][0]['error-text']}")


sendSMS("+41779611539", 2, "hi")
