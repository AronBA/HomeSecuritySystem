from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import ssl
import smtplib

password = ''


def sendemail(cameraNumber: int, receiver: str, sender: str, msg: str, subject: str, imgPath: str = ""):
    em = MIMEMultipart('alternative')
    em['from'] = sender
    em['To'] = receiver
    em['Subject'] = subject

    if imgPath != "":
        with open(imgPath, "rb") as IF:
            f = IF.read()
            image = bytes(f)
        text = MIMEText(f"""<p>*******************************************</p>
<p>There was motion detected by camera #{cameraNumber}</p>
<p>*******************************************</p>
<p>{msg}</p>
<img src="cid:attachedImg">
""", 'html')
        em.attach(text)
        img = MIMEImage(image)
        img.add_header('Content-ID', 'attachedImg')
        em.attach(img)
    else:
        text = MIMEText(f"""<p>*******************************************</p>
        <p>There was motion detected by camera #{cameraNumber}</p>
        <p>*******************************************</p>
        <p>{msg}</p>
        """, 'html')
        em.attach(text)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender, password)
        smtp.sendmail(sender, receiver, em.as_string())
