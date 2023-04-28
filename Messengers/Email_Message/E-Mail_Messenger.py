from email.message import EmailMessage
import ssl
import smtplib

password = ''


def sendemail(cameraNumber: int, receiver: str, sender: str, msg: str, subject: str):
    text = f"""*******************************************
There was motion detected by camera #{cameraNumber}
*******************************************
{msg}"""
    em = EmailMessage()
    em['from'] = sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(text)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender,receiver, em.as_string())
