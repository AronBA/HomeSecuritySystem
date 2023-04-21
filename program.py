import tkinter as tk
from configparser import ConfigParser
import os

config = ConfigParser()


def save(Delay="", RTSP="", Website="", Program=""):
    config.set("DEFAULT", "Delay", Delay)
    config.set("DEFAULT", "RTSP", RTSP)
    config.set("DEFAULT", "Program", Program)
    config.set("DEFAULT", "Website", Website)
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


def showMessenger(state):
    if state:
        messengerFrame.grid(row=1, column=0, padx=25)
    else:
        messengerFrame.grid_remove()


root = tk.Tk()

root.title("Settings")
root.resizable(False, False)
root.geometry("600x400")
root.eval('tk::PlaceWindow . center')

frame = tk.Frame(root)
frame.pack()
contentFrame = tk.LabelFrame(frame, text="Settings")
contentFrame.grid(row=0, column=0, padx=25)

emailFrame = tk.LabelFrame(frame, text="Email")
emailFrame.grid_remove()

messengerFrame = tk.LabelFrame(frame, text="Messenger")
messengerFrame.grid_remove()

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
messageState = tk.BooleanVar()
sendEmailLabel = tk.Label(contentFrame, text="Send Email")
sendEmail = tk.Checkbutton(contentFrame, onvalue=1, offvalue=0, variable=emailState,
                           command=lambda: showEmail(emailState.get()))
sendMessengerLabel = tk.Label(contentFrame, text="Send Message")
sendMessenger = tk.Checkbutton(contentFrame, onvalue=1, offvalue=0, variable=messageState,
                               command=lambda: showMessenger(messageState.get()))


# Content for Email Frame
emailAddressLabel = tk.Label(emailFrame, text="Email Address")
emailAddress = tk.Entry(emailFrame)
emailSubjectLabel = tk.Label(emailFrame, text="Email Subject")
emailSubject = tk.Entry(emailFrame)
emailContentLabel = tk.Label(emailFrame, text="Email Content")
emailContent = tk.Text(emailFrame, height=5, width=15)

# Content for Messenger Frame
messengerNumberLabel = tk.Label(messengerFrame, text="Tel. Number")
messengerNumber = tk.Entry(messengerFrame)
messengerTextLabel = tk.Label(messengerFrame, text="Messenger Text")
messengerText = tk.Entry(messengerFrame)

# Add the items to the Frame
contentItems = [[rtpsLabel, rtps], [programLabel, program], [websiteLabel, website], [delayLabel, delay],
                [sendEmailLabel, sendEmail], [sendMessengerLabel, sendMessenger]]
emailItems = [[emailAddressLabel, emailAddress], [emailSubjectLabel, emailSubject], [emailContentLabel, emailContent]]
messengerItems = [[messengerNumberLabel, messengerNumber], [messengerTextLabel, messengerText]]
addInputs(contentItems)
addInputs(emailItems)
addInputs(messengerItems)

saveButton = tk.Button(text="save&restart", command=lambda: save(delay.get(), rtps.get(), program.get(), website.get()))
saveButton.pack()

root.mainloop()

# Mes. Bigger input field, Delay einheit, Definitions
