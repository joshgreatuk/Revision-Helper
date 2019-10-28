import PySimpleGUI as gui
from subprocess import Popen
import os
gui.ChangeLookAndFeel("BlueMono")
layout = [[gui.Text("Welcome To Revision Helper",size=(50,2))], [gui.Button("Notes",button_color=('white','blue')), gui.Button("Flash Cards",button_color=('white','blue')), gui.Button("Exit",button_color=('white','red'))]]
window = gui.Window("Revision Helper",layout=layout,resizable=False)
window.read(timeout=1)
while True:
    event, values = window.read()
    if event in (None,"Exit"):
        break
    elif event in ("Notes"):
        if os.path.exists("Notes.pyw"):
            Popen("python Notes.pyw")
        elif os.path.exists("Notes.exe"):
            Popen("Notes.exe")
    elif event in ("Flash Cards"):
        if os.path.exists("Notes.pyw"):
            Popen("python Cards.pyw")
        elif os.path.exists("Notes.exe"):
            Popen("Cards.exe")
window.close()
