import smtplib

mainEmail = 'C.A.S@HomeAlertSystem.com'
client = ['klemenzmahar@gmail.com']

camera = '#1'


def sendemail(cameraNumber: int, receiver: [str], sender: str):
    receivers = ""
    for rec in receiver:
        receivers += ", " + rec
    message = f"""From: C.A.S <{sender}>
    To: {receivers}
    Subject: Motion Detected

    There was motion detected by camera #{cameraNumber}
    """
    try:
        smtpobj = smtplib.SMTP('localhost')
        smtpobj.sendmail(sender, receiver, message)
        print('Email Sent')
    except smtplib.SMTPException or smtplib.SMTPResponseException or smtplib.SMTPRecipientsRefused or smtplib.SMTPSenderRefused or smtplib.SMTPHeloError as error:
        print(error)


sendemail(1, client, mainEmail)
