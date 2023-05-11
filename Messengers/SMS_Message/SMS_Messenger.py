import vonage
import json
from parser.fileParser import getProjFile

data = json.load(open(getProjFile("config.json")))["sms"]
secret = data["smsSecret"]
key = data["smsKey"]
client = vonage.Client(key=key, secret=secret)
sms = vonage.Sms(client=client)
recipient = data["smsNumber"]
msg = data["smsText"]


def sendSMS(cameraNum: int):
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
