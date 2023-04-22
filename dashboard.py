import tkinter as tk
from configparser import ConfigParser
import os
import subprocess

config = ConfigParser()
process = None

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
    with open('Files/settings.ini', 'w') as f:
        config.write(f)


def run():
    arg = ["/home/aron/PycharmProjects/Modularbeit426/Motiondetection/motiondetection.py"]
    path = "/usr/bin/python3"
    global process
    process=subprocess.Popen([path] + arg)




def stop(process):
    if process is not None:
        process.terminate()



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
messengerState = tk.BooleanVar()
sendEmailLabel = tk.Label(contentFrame, text="Send Email")
sendEmail = tk.Checkbutton(contentFrame, onvalue=1, offvalue=0, variable=emailState,
                           command=lambda: showEmail(emailState.get()))
sendMessengerLabel = tk.Label(contentFrame, text="Send Message")
sendMessenger = tk.Checkbutton(contentFrame, onvalue=1, offvalue=0, variable=messengerState,
                               command=lambda: showMessenger(messengerState.get()))


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
messengerContentLabel = tk.Label(messengerFrame, text="Messenger Text")
messengerContent = tk.Text(messengerFrame, height=5, width=15)

# Add the items to the Frame
contentItems = [[rtpsLabel, rtps], [programLabel, program], [websiteLabel, website], [delayLabel, delay],
                [sendEmailLabel, sendEmail], [sendMessengerLabel, sendMessenger]]
emailItems = [[emailAddressLabel, emailAddress], [emailSubjectLabel, emailSubject], [emailContentLabel, emailContent]]
messengerItems = [[messengerNumberLabel, messengerNumber], [messengerContentLabel, messengerContent]]
addInputs(contentItems)
addInputs(emailItems)
addInputs(messengerItems)

saveButton = tk.Button(text="Save", command=lambda: save(delay.get(), rtps.get(), program.get(), website.get(),
                                                         emailState.get(), emailAddress.get(), emailSubject.get(),
                                                         emailContent.get(1.0, "end-1c"),
                                                         messengerState.get(), messengerNumber.get(),
                                                         messengerContent.get(1.0, "end-1c")))
runButton = tk.Button(text="run",command=run)
stopbutton = tk.Button(text="stop",command=lambda: stop(process))

stopbutton.pack()
runButton.pack()
saveButton.pack()

root.mainloop()
