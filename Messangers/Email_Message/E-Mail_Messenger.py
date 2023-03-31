import smtplib

sender = 'C.A.S@HomeAlerts.com'
client = ['yourEmailAdresses']

camera = '#1'


def sendemail(cameraNumber: int, receiver: str):
    message = f"""From: C.A.S <{sender}>
    To: {receiver}
    Subject: Motion Detected

    There was motion detected by camera #{cameraNumber}
    """
    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receiver, message)
        print('Success')
    except smtplib.SMTPException:
        print('Email not sent')

sendemail(1, 'klemenzmahar@gmail.com')