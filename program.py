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


root = tk.Tk()

root.title("Settings")
root.resizable(False, False)
root.geometry("600x400")
root.eval('tk::PlaceWindow . center')

contentPanel = tk.PanedWindow()
emailPanel = tk.PanedWindow()

rtpsLabel = tk.Label(text="RTPS")
rtps = tk.Entry(root)

programLabel = tk.Label(text="Programm")
program = tk.Entry(root)

websiteLabel = tk.Label(text="website")
website = tk.Entry(root)

delayLabel = tk.Label(text="delay")
delay = tk.Entry(root)

emailAdressLabel = tk.Label(text="Email Adresse")
emailAdress = tk.Entry(root)

b = tk.Button(text="save&restart", command=lambda: save(delay.get(), rtps.get(), program.get(), website.get()))

contentPanel.add(rtpsLabel)
contentPanel.add(rtps)
contentPanel.add(programLabel)
contentPanel.add(program)

emailPanel.add(emailAdressLabel)
emailPanel.add(emailAdress)

contentPanel.pack(side="left")
emailPanel.pack(side="right")
b.pack(side="bottom")

root.mainloop()
