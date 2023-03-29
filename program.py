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

l = tk.Label(text="RTPS")
url = tk.Entry(root, text="sex")

l2 = tk.Label(text="delay")
dealay2 = tk.Entry(root)

l3 = tk.Label(text="programm")
programm = tk.Entry(root)

l4 = tk.Label(text="website")
website = tk.Entry(root)

b = tk.Button(text="save&restart", command=lambda: save(dealay2.get(), url.get(), programm.get(), website.get()))

l.pack()
url.pack()
l2.pack()
dealay2.pack()
l3.pack()
programm.pack()
l4.pack()
website.pack()

b.pack()

root.mainloop()
