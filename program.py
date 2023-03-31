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
        item[0].grid(row=idx, column=0, pady=5)
        item[1].grid(row=idx, column=1, pady=5)

def showEmail(state):
    if state:
        emailFrame.grid(row=0, column=1)
    else:
        emailFrame.grid_remove()

root = tk.Tk()

root.title("Settings")
root.resizable(False, False)
root.geometry("600x400")
root.eval('tk::PlaceWindow . center')

frame = tk.Frame(root)
frame.pack()
contentFrame = tk.LabelFrame(frame, text="Einstellungen")
contentFrame.grid(row=0, column=0)

emailFrame = tk.LabelFrame(frame, text="Email")
emailFrame.grid(row=0, column=1)

# Content for Content Frame
rtpsLabel = tk.Label(contentFrame, text="RTPS")
rtps = tk.Entry(contentFrame)
programLabel = tk.Label(contentFrame, text="Programm")
program = tk.Entry(contentFrame)
websiteLabel = tk.Label(contentFrame, text="Website")
website = tk.Entry(contentFrame)
delayLabel = tk.Label(contentFrame, text="Delay")
delay = tk.Entry(contentFrame)
sendEmailLabel = tk.Label(contentFrame, text="Delay")
sendEmail = tk.Checkbutton(contentFrame, onvalue=1, offvalue=0)

# Content for Email Frame
emailAdressLabel = tk.Label(emailFrame, text="Email Adresse")
emailAdress = tk.Entry(emailFrame)
emailSubjectLabel = tk.Label(emailFrame, text="Email Subject")
emailSubject = tk.Entry(emailFrame)
emailContentLabel = tk.Label(emailFrame, text="Email Content")
emailContent = tk.Text(emailFrame, height=5, width=15)

# Add the items to the Frame
contentItems = [[rtpsLabel,rtps],[programLabel,program],[websiteLabel,website],[delayLabel,delay],[sendEmailLabel, sendEmail]]
emailItems = [[emailAdressLabel,emailAdress],[emailSubjectLabel, emailSubject],[emailContentLabel,emailContent]]
addInputs(contentItems)
addInputs(emailItems)


saveButton = tk.Button(text="save&restart", command=lambda: save(delay.get(), rtps.get(), program.get(), website.get()))


root.mainloop()
