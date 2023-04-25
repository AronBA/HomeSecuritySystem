import tkinter as tk
from configparser import ConfigParser
import os

config = ConfigParser()


def save(Delay="", RTSP="", Website="", Program="",
         EmailState=False, EmailAdress="", EmailSubject="", EmailContent="",
         MessengerState=False, MessengerNumber="", MessengerContent=""):
    config.set("DEFAULT", "Delay", Delay)
    config.set("DEFAULT", "RTSP", RTSP)
    config.set("DEFAULT", "Program", Program)
    config.set("DEFAULT", "Website", Website)
    config.set("DEFAULT", "EmailState", f"{EmailState}")
    config.set("DEFAULT", "EmailAddress", EmailAdress)
    config.set("DEFAULT", "EmailSubject", EmailSubject)
    config.set("DEFAULT", "EmailContent", EmailContent)
    config.set("DEFAULT", "MessengerState", f"{MessengerState}")
    config.set("DEFAULT", "MessengerNumber", MessengerNumber)
    config.set("DEFAULT", "MessengerContent", MessengerContent)
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

# Content for Content Frame
rtpsLabel = tk.Label(contentFrame, text="RTPS")
rtps = tk.Entry(contentFrame)
programLabel = tk.Label(contentFrame, text="Program")
program = tk.Entry(contentFrame)
websiteLabel = tk.Label(contentFrame, text="Website")
website = tk.Entry(contentFrame)
delayLabel = tk.Label(contentFrame, text="Delay")
delay = tk.Entry(contentFrame)
emailState = tk.BooleanVar()
smsState = tk.BooleanVar()
sendEmailLabel = tk.Label(contentFrame, text="Send Email")
sendEmail = tk.Checkbutton(contentFrame, onvalue=1, offvalue=0, variable=emailState,
                           command=lambda: showEmail(emailState.get()))
sendSmsLabel = tk.Label(contentFrame, text="Send Message")
sendSms = tk.Checkbutton(contentFrame, onvalue=1, offvalue=0, variable=smsState,
                         command=lambda: showSms(smsState.get()))


# Content for Email Frame
emailPasswordLabel = tk.Label(emailFrame, text="Email Password")
emailPassword = tk.Entry(emailFrame, show="*")
emailAddressLabel = tk.Label(emailFrame, text="Email Address")
emailAddress = tk.Entry(emailFrame)
emailSubjectLabel = tk.Label(emailFrame, text="Email Subject")
emailSubject = tk.Entry(emailFrame)
emailContentLabel = tk.Label(emailFrame, text="Email Content")
emailContent = tk.Text(emailFrame, height=5, width=15)

# Content for SMS Frame
smsSecretLabel = tk.Label(smsFrame, text="SMS Secret")
smsSecret = tk.Entry(smsFrame)
smsKeyLabel = tk.Label(smsFrame, text="SMS Key")
smsKey = tk.Entry(smsFrame)
smsNumberLabel = tk.Label(smsFrame, text="Tel. Number")
smsNumber = tk.Entry(smsFrame)
smsContentLabel = tk.Label(smsFrame, text="SMS Text")
smsContent = tk.Text(smsFrame, height=5, width=15)

# Add the items to the Frame
contentItems = [[rtpsLabel, rtps], [programLabel, program], [websiteLabel, website], [delayLabel, delay],
                [sendEmailLabel, sendEmail], [sendSmsLabel, sendSms]]
emailItems = [[emailPasswordLabel, emailPassword], [emailAddressLabel, emailAddress], [emailSubjectLabel, emailSubject],
              [emailContentLabel, emailContent]]
smsItems = [[smsSecretLabel, smsSecret], [smsKeyLabel, smsKey], [smsNumberLabel, smsNumber],
            [smsContentLabel, smsContent]]
addInputs(contentItems)
addInputs(emailItems)
addInputs(smsItems)

saveButton = tk.Button(text="Save", command=lambda: save(delay.get(), rtps.get(), program.get(), website.get(),
                                                         emailState.get(), emailAddress.get(), emailSubject.get(),
                                                         emailContent.get(1.0, "end-1c"),
                                                         smsState.get(), smsNumber.get(),
                                                         smsContent.get(1.0, "end-1c")))
saveButton.pack()

root.mainloop()
