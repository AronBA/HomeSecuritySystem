import tkinter as tk
from configparser import ConfigParser
import os

config = ConfigParser()


def save(Delay="", RTSP="", Website="", Program="",
         EmailState=0, EmailPassword="", EmailAdress="", EmailSubject="", EmailContent="",
         SmsState=0, SmsSecret="", SmsKey="", SmsNumber="", SmsContent=""):
    config.set("DEFAULT", "Delay", Delay)
    config.set("DEFAULT", "RTSP", RTSP)
    config.set("DEFAULT", "Program", Program)
    config.set("DEFAULT", "Website", Website)
    config.set("DEFAULT", "EmailState", f"{EmailState}")
    config.set("DEFAULT", "EmailPassword", EmailPassword)
    config.set("DEFAULT", "EmailAddress", EmailAdress)
    config.set("DEFAULT", "EmailSubject", EmailSubject)
    config.set("DEFAULT", "EmailContent", EmailContent)
    config.set("DEFAULT", "smsState", f"{SmsState}")
    config.set("DEFAULT", "smssecret", SmsSecret)
    config.set("DEFAULT", "smskey", SmsKey)
    config.set("DEFAULT", "smsNumber", SmsNumber)
    config.set("DEFAULT", "smsContent", SmsContent)
    with open('settings.ini', 'w') as f:
        config.write(f)

    os.system("main.py")


def addInputs(items):
    for idx, item in enumerate(items):
        item[0].grid(row=idx, column=0, pady=5, padx=5, sticky="W")
        item[1].grid(row=idx, column=1, pady=5, padx=5, sticky="W")


def showEmail(state):
    if state:
        emailFrame.grid(row=0, column=1, padx=25)
    else:
        emailFrame.grid_remove()


def showSms(state):
    if state:
        smsFrame.grid(row=1, column=0, padx=25)
    else:
        smsFrame.grid_remove()


root = tk.Tk()

root.title("Settings")
root.resizable(False, False)
root.geometry("750x500")
root.eval('tk::PlaceWindow . center')

frame = tk.Frame(root)
frame.pack()
contentFrame = tk.LabelFrame(frame, text="Settings")
contentFrame.grid(row=0, column=0, padx=25)

emailFrame = tk.LabelFrame(frame, text="Email")
emailFrame.grid_remove()

smsFrame = tk.LabelFrame(frame, text="SMS")
smsFrame.grid_remove()

config.read("settings.ini")
# Content for Content Frame
rtspLabel = tk.Label(contentFrame, text="RTPS")
rtsp = tk.Entry(contentFrame)
rtsp.insert(0, config.get("DEFAULT", "rtsp"))
programLabel = tk.Label(contentFrame, text="Program")
program = tk.Entry(contentFrame)
program.insert(0, config.get("DEFAULT", "program"))
websiteLabel = tk.Label(contentFrame, text="Website")
website = tk.Entry(contentFrame)
website.insert(0, config.get("DEFAULT", "website"))
delayLabel = tk.Label(contentFrame, text="Delay")
delay = tk.Entry(contentFrame)
delay.insert(0, config.get("DEFAULT", "delay"))
emailState = tk.IntVar(value=int(config.get("DEFAULT", "emailState")))
if emailState.get():
    showEmail(True)
smsState = tk.IntVar(value=int(config.get("DEFAULT", "smsState")))
if smsState.get():
    showSms(True)
sendEmailLabel = tk.Label(contentFrame, text="Send Email")
sendEmail = tk.Checkbutton(contentFrame, onvalue=1, offvalue=0, variable=emailState,
                           command=lambda: showEmail(emailState.get()))
sendSmsLabel = tk.Label(contentFrame, text="Send Message")
sendSms = tk.Checkbutton(contentFrame, onvalue=1, offvalue=0, variable=smsState,
                         command=lambda: showSms(smsState.get()))


# Content for Email Frame
emailPasswordLabel = tk.Label(emailFrame, text="Email Password")
emailPassword = tk.Entry(emailFrame, show="*")
emailPassword.insert(0, config.get("DEFAULT", "emailpassword"))
emailAddressLabel = tk.Label(emailFrame, text="Email Address")
emailAddress = tk.Entry(emailFrame)
emailAddress.insert(0, config.get("DEFAULT", "emailaddress"))
emailSubjectLabel = tk.Label(emailFrame, text="Email Subject")
emailSubject = tk.Entry(emailFrame)
emailSubject.insert(0, config.get("DEFAULT", "emailsubject"))
emailContentLabel = tk.Label(emailFrame, text="Email Content")
emailContent = tk.Text(emailFrame, height=5, width=15)
emailContent.insert(tk.INSERT, config.get("DEFAULT", "emailcontent"))

# Content for SMS Frame
smsSecretLabel = tk.Label(smsFrame, text="SMS Secret")
smsSecret = tk.Entry(smsFrame)
smsSecret.insert(0, config.get("DEFAULT", "smssecret"))
smsKeyLabel = tk.Label(smsFrame, text="SMS Key")
smsKey = tk.Entry(smsFrame)
smsKey.insert(0, config.get("DEFAULT", "smskey"))
smsNumberLabel = tk.Label(smsFrame, text="Tel. Number")
smsNumber = tk.Entry(smsFrame)
smsNumber.insert(0, config.get("DEFAULT", "smsnumber"))
smsContentLabel = tk.Label(smsFrame, text="SMS Text")
smsContent = tk.Text(smsFrame, height=5, width=15)
smsContent.insert(tk.INSERT, config.get("DEFAULT", "smscontent"))

# Add the items to the Frame
contentItems = [[rtspLabel, rtsp], [programLabel, program], [websiteLabel, website], [delayLabel, delay],
                [sendEmailLabel, sendEmail], [sendSmsLabel, sendSms]]
emailItems = [[emailPasswordLabel, emailPassword], [emailAddressLabel, emailAddress], [emailSubjectLabel, emailSubject],
              [emailContentLabel, emailContent]]
smsItems = [[smsSecretLabel, smsSecret], [smsKeyLabel, smsKey], [smsNumberLabel, smsNumber],
            [smsContentLabel, smsContent]]
addInputs(contentItems)
addInputs(emailItems)
addInputs(smsItems)

saveButton = tk.Button(text="Save", command=lambda: save(delay.get(), rtsp.get(), program.get(), website.get(),
                                                         emailState.get(), emailPassword.get(), emailAddress.get(),
                                                         emailSubject.get(), emailContent.get(1.0, "end-1c"),
                                                         smsState.get(), smsSecret.get(), smsKey.get(),
                                                         smsNumber.get(), smsContent.get(1.0, "end-1c")))
saveButton.pack()

root.mainloop()
