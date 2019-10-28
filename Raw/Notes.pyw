import PySimpleGUI as gui
import os

#Create Notepad Window
currentsubject = "No Subject"
currenttopic = "No Topic"
gui.ChangeLookAndFeel("BlueMono")
subtreedata = gui.TreeData()
toptreedata = gui.TreeData()
layout = [[gui.Text(text=currentsubject,font=("Consolas",10),size=(25,1),key="subject"), gui.Text(text=currenttopic,font=("Consolas",10),size=(25,1),key="topic"), gui.Button("New Topic"), gui.Button("Save Topic"), gui.Button("Change Topic"),gui.Button("Delete Topic"), gui.Button("New Subject"), gui.Button("Change Subject"), gui.Button("Delete Subject"), gui.Button("Exit")], [gui.Tree(data=subtreedata,headings=[],auto_size_columns=False,col0_width=15,num_rows=27,key="subtree",enable_events=True), gui.Tree(data=toptreedata,headings=[],auto_size_columns=False,col0_width=15,num_rows=27,key="toptree",enable_events=True), gui.Multiline(font=("Consolas",12),size=(100,30),key="body")]]

window = gui.Window("Revision Helper : Notes",layout=layout,margins=(0,0),resizable=False)
window.read(timeout=1)

#Functions
def UpdateTree():
    subfiles = os.listdir("Notes/")
    subtreedata = gui.TreeData()
    parent = ""
    for i in subfiles:
        subtreedata.Insert(parent=parent,text=i,values=[],key=i)
    window.FindElement("subtree").Update(values=subtreedata)
    if currentsubject != "No Subject":
        topfiles = os.listdir(("Notes/"+currentsubject+"/"))
        toptreedata = gui.TreeData()
        for i in topfiles:
            toptreedata.Insert(parent=parent,text=i,values=[],key=i)
        window.FindElement("toptree").Update(values=toptreedata)
UpdateTree()

#Event Loop
while True:
    event,values = window.read()
    if event in (None,"Cancel"):
        break
    elif event in ("Exit"):
        break
    elif event in ("New Subject"):
        new = gui.popup_get_text("Enter New Subject Name")
        if new.strip() != "":
            new = new.lower()
            os.mkdir("Notes/"+new)
            window.FindElement("subject").Update(value=new)
            currentsubject=new
            currenttopic="No Topic"
            window.FindElement("topic").Update(value="No Topic")
            UpdateTree()
        else:
            gui.popup_error("Entered Nothing")
    elif event in ("Delete Subject"):
        new = gui.popup_get_text("Enter Subject To Delete")
        if new.strip() != "":
            new = new.lower()
            if os.path.exists("Notes/"+new):
                os.rmdir("Notes/"+new)
                currentsubject = "No Subject"
                currenttopic = "No Topic"
                UpdateTree()
                window.FindElement("subject").Update(value="No Subject")
                window.FindElement("topic").Update(value="No Topic")
        else:
            gui.popup_error("Entered Nothing")
    elif event in ("Change Subject"):
        new = gui.popup_get_text("Enter Subject To Change To")
        if new.strip() != "":
            new = new.lower()
            if os.path.exists("Notes/"+new):
                currentsubject=new
                currenttopic="No Topic"
                UpdateTree()
                window.FindElement("subject").Update(value=new)
                window.FindElement("topic").Update(value="No Topic")
            else:
                gui.popup_error("Couldnt Find Subject")
        else:
            gui.popup_error("Entered Nothing")
    elif event in ("New Topic"):
        new = gui.popup_get_text("Enter New Topic Name")
        if new.strip() != "":
            new = new.lower()
            f = open("Notes/"+currentsubject+"/"+new,"w")
            f.write("")
            f.close()
            currenttopic = new
            window.FindElement("topic").Update(value=new)
            with open(("Notes/"+currentsubject+"/"+new),"r") as f:
                window.FindElement("body").Update(f.read())
            UpdateTree()
        else:
            gui.popup_error("Entered Nothing")
    elif event in ("Delete Topic"):
        new = gui.popup_get_text("Enter Topic To Delete")
        if new.strip() != "":
            new = new.lower()
            if os.path.exists("Notes/"+currentsubject+"/"+new):
                os.remove("Notes/"+currentsubject+"/"+new)
                UpdateTree()
                window.FindElement("topic").Update(value="No Topic")
        else:
            gui.popup_error("Entered Nothing")
    elif event in ("Change Topic"):
        new = gui.popup_get_text("Enter Topic To Change To")
        if new.strip() != "":
            new = new.lower()
            if os.path.exists("Notes/"+currentsubject+"/"+new):
                currenttopic=new
                UpdateTree()
                window.FindElement("topic").Update(value=new)
                with open(("Notes/"+currentsubject+"/"+new),"r") as f:
                    window.FindElement("body").Update(f.read())
        else:
            gui.popup_error("Entered Nothing")
    elif event in ("Save Topic"):
        if currenttopic != "No Topic":
            with open(("Notes/"+currentsubject+"/"+currenttopic),"w") as f:
                f.write(values.get("body"))
            gui.popup_ok("Topic Saved")

window.close()
