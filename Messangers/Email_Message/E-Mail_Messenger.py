import smtplib

mainSender = 'C.A.S@HomeAlertSystem.com'
mainReceivers = ['klemenzmahar@gmail.com']
mainMsg = "movement detected"
camera = "#1"
mainSubject = "Motion Detected"


def sendemail(cameraNumber: int, receiver: [str], sender: str, msg: str, subject: str):
    receivers = ""
    for rec in receiver:
        receivers += ", " + rec
    message = f"""From: C.A.S <{sender}>
    To: {receivers}
    Subject: {subject}
    
    {msg}
    There was motion detected by camera #{cameraNumber}
    """
    try:
        smtpobj = smtplib.SMTP('localhost')
        smtpobj.sendmail(sender, receiver, message)
        print('Email Sent')
    except smtplib.SMTPException or smtplib.SMTPResponseException or smtplib.SMTPRecipientsRefused or smtplib.SMTPSenderRefused or smtplib.SMTPHeloError as error:
        print(error)


sendemail(1, mainReceivers, mainSender, mainMsg, mainSubject)
