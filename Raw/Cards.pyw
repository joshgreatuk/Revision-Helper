import PySimpleGUI as gui
import os
import random

#Create Cards window
currentsubject = "No Subject"
gui.ChangeLookAndFeel("BlueMono")
subtreedata = gui.TreeData()
data = []
layout = [[gui.Button("New Subject"),gui.Button("Change Subject"),gui.Button("Delete Subject"),gui.Button("Show Random Card"),gui.Button("New Card"),gui.Button("Modify Card"),gui.Button("Delete Card"),gui.Button("Exit")],[gui.Text(text="Subjects",font=("Consolas",10),size=(60,1),key="subject"), gui.Text(text=currentsubject,font=("Consolas",10),size=(40,1),key="currentsubject")], [gui.Tree(data=subtreedata,headings=[],auto_size_columns=False,col0_width=15,num_rows=27,key="subtree",enable_events=True), gui.Table(values=data[1:][:],headings=["Topic","Question"],col_widths=[20,40],auto_size_columns=False,display_row_numbers=False,num_rows=27,key="cardtable",select_mode="browse",alternating_row_color="LightBlue",justification="centre")]]
window = gui.Window("Revision Helper : Cards",layout=layout,margins=(0,0),resizable=True)
window.read(timeout=1)

#Functions
def FlashCard():
    #Gets a random topic then question from that topic
    if currentsubject != "No Subject":
        topics = os.listdir("Cards/"+currentsubject+"/")
        questions = []
        for i in topics:
            for j in os.listdir("Cards/"+currentsubject+"/"+i+"/"):
                questions.append([j,i])
        questionnum = random.randint(1,len(questions))-1
        question = questions[questionnum][0]
        questiontopic = questions[questionnum][1]
        f = open("Cards/"+currentsubject+"/"+questiontopic+"/"+question)
        answer = f.read()
        f.close()
        flashlayout = [[gui.Text(text="Question:",key="toptext",size=(50,2))], [gui.Text(text=question,key="questiontext",size=(50,5))], [gui.Button("Answer",key="ansbut"),gui.Button("Cancel",key="canbut")]]
        flashwindow = gui.Window("Revision Helper : Flash Card",layout=flashlayout,margins=(0,0),resizable=False)
        another = False
        cardmode = 1
        print(question)
        print(answer)
        while True:
            event, values = flashwindow.read()
            if event in (None,"canbut"):
                flashwindow.close()
                break
            elif event in ("ansbut"):
                if cardmode == 1:
                    flashwindow["toptext"].Update(value="Answer:")
                    flashwindow["questiontext"].Update(value=answer)
                    flashwindow["ansbut"].Update(text="Another")
                    flashwindow["canbut"].Update(text="Done")
                    cardmode = 2
                elif cardmode == 2:
                    another = True
                    flashwindow.close()
                    break
        if another:
            FlashCard()
        window.Enable()

def UpdateTree():
    subfiles = os.listdir("Cards/")
    subtreedata = gui.TreeData()
    parent = ""
    for i in subfiles:
        subtreedata.Insert(parent=parent,text=i,values=[],key=i)
    window.FindElement("subtree").Update(values=subtreedata)
    if currentsubject != "No Subject":
        topfiles = os.listdir("Cards/"+currentsubject+"/")
        toptabledata = []
        for i in range(len(topfiles)):
            quefiles = os.listdir("Cards/"+currentsubject+"/"+topfiles[i])
            for j in range(len(quefiles)):
                toptabledata.append([topfiles[i],quefiles[j]])
        window.FindElement("cardtable").Update(values=toptabledata)
UpdateTree()

#Event Loop

while True:
    event,values = window.read()
    if event in (None,"Cancel") or event in ("Exit"):
        break
    elif event in ("New Subject"):
        new = gui.popup_get_text("Enter New Subject Name")
        if new.strip() != "":
            new = new.lower()
            os.mkdir("Cards/"+new)
            window.FindElement("currentsubject").Update(value="Subject : "+new)
            currentsubject=new
            UpdateTree()
        else:
            gui.popup_error("Entered Nothing")
    elif event in ("Change Subject"):
        new = gui.popup_get_text("Enter Subject To Change To")
        if new.strip() != "":
            new = new.lower()
            if os.path.exists("Cards/"+new):
                currentsubject=new
                window.FindElement("currentsubject").Update(value="Subject : "+new)
                UpdateTree()
        else:
            gui.popup_error("Entered Nothing")
    elif event in ("Delete Subject"):
        new = gui.popup_get_text("Enter Subject To Delete")
        if new.strip() != "":
            new = new.lower()
            if os.path.exists("Cards/"+new):
                for i in os.listdir("Cards/"+new+"/"):
                    os.rmdir("Cards/"+new+"/"+i+"/")
                os.rmdir("Cards/"+new)
                currentsubject = "No Subject"
                window.FindElement("currentsubject").Update(value="No Subject")
                UpdateTree()
        else:
            gui.popup_error("Entered Nothing")
    elif event in ("Show Random Card"):
        FlashCard()
    elif event in ("New Card"):
        if currentsubject != "No Subject":
            cardlayout = [[gui.Text(text="Flash Card Creator",key="toptext")], [gui.Text(text="Topic",key="topictext")], [gui.Input("",key="topicentry",enable_events=True)], [gui.Text(text="Question (no special characters '/','?')",key="questiontext")], [gui.Input("",key="questionentry",enable_events=True)], [gui.Text(text="Answer",key="answertext")], [gui.Input("",key="answerentry",enable_events=True)],  [gui.Button("Create Card")]]
            cardwindow = gui.Window("Revision Helper : Card Creator",layout=cardlayout,margins=(0,0),resizable=False)
            cardwindow.read()
            while True:
                event, values = cardwindow.read()
                if event in (None,"Cancel"):
                    break
                elif event in ("Create Card"):
                    if (cardwindow["topicentry"].get()).strip() != "" and (cardwindow["questionentry"].get()).strip() != "" and (cardwindow["answerentry"].get()).strip() != "":
                        if os.path.exists("Cards/"+currentsubject+"/"+cardwindow["topicentry"].get()) == False:
                            os.mkdir("Cards/"+currentsubject+"/"+cardwindow["topicentry"].get())
                        f = open("Cards/"+currentsubject+"/"+cardwindow["topicentry"].get() +"/"+cardwindow["questionentry"].get(),"w")
                        f.write(cardwindow["questionentry"].get()+"\n\n"+cardwindow["answerentry"].get())
                        f.close()
                        UpdateTree()
                        break
                    else:
                        gui.popup_error("Enter Values")
            cardwindow.close()
        else:
            gui.popup_error("Choose A Subject First")
    elif event in ("Modify Card"):
        if currentsubject != "No Subject":
            cardlayout = [[gui.Text(text="Flash Card Modifier",key="toptext")], [gui.Text(text="Topic Of Question",key="topictext")], [gui.Input("",key="topicentry",enable_events=True)], [gui.Text(text="Question To Modify",key="questiontext")], [gui.Input("",key="questionentry",enable_events=True)], [gui.Button("Modify Card")]]
            cardwindow = gui.Window("Revision Helper : Card Modifier",layout=cardlayout,margins=(0,0),resizable=False)
            cardwindow.read()
            while True:
                event, values = cardwindow.read()
                if event in (None,"Cancel"):
                    break
                elif event in ("Modify Card"):
                    if (cardwindow["topicentry"].get()).strip() != "" and (cardwindow["questionentry"].get()).strip() != "":
                        topicmodify = cardwindow["topicentry"].get()
                        questionmodify = cardwindow["questionentry"].get()
                        break
            #modifier window
            cardlayout = [[gui.Text(text="Flash Card Modifier",key="toptext")], [gui.Text(text="Topic",key="topictext")], [gui.Input("",key="topicentry",enable_events=True)], [gui.Text(text="Question (no special characters '/','?')",key="questiontext")], [gui.Input("",key="questionentry",enable_events=True)], [gui.Text(text="Answer",key="answertext")], [gui.Input("",key="answerentry",enable_events=True)],  [gui.Button("Modify Card")]]
            cardwindow = gui.Window("Revision Helper : Card Modifier",layout=cardlayout,margins=(0,0),resizable=False)
            f = open("Cards/"+currentsubject+"/"+topicmodify+"/"+questionmodify,"r")
            question = f.readline()
            answer = f.readline()
            f.close()
            cardwindow.read()
            cardwindow["topicentry"].Update(value=topicmodify)
            cardwindow["questionentry"].Update(value=question)
            cardwindow["answerentry"].Update(value=answer)
            cardwindow.read()
            while True:
                event, values = cardwindow.read()
                if event in (None,"Cancel"):
                    break
                elif event in ("Modify Card"):
                    if (cardwindow["topicentry"].get()).strip() != "" and (cardwindow["questionentry"].get()).strip() != "" and (cardwindow["answerentry"].get()).strip() != "":
                        os.remove("Cards/"+currentsubject+"/"+topicmodify+"/"+questionmodify)
                        if not os.path.exists("Cards/"+currentsubject+"/"+cardwindow["topicentry"].get()):
                            os.mkdir("Cards/"+currentsubject+"/"+cardwindow["topicentry"].get())
                        f = open("Cards/"+currentsubject+"/"+cardwindow["topicentry"].get() +"/"+cardwindow["questionentry"].get().strip(),"w")
                        f.write(cardwindow["questionentry"].get()+"\n\n"+cardwindow["answerentry"].get().strip())
                        f.close()
                        UpdateTree()
                        if len(os.listdir("Cards/"+currentsubject+"/"+topicmodify+"/")) == 0:
                            os.rmdir("Cards/"+currentsubject+"/"+topicmodify+"/")
                        break
                    else:
                        gui.popup_error("Enter Values")
            cardwindow.close()
        else:
            gui.popup_error("Choose A Subject First")
    elif event in ("Delete Card"):
        if currentsubject != "No Subject":
            cardlayout = [[gui.Text(text="Flash Card Deleter",key="toptext")], [gui.Text(text="Topic",key="topictext")], [gui.Input("",key="topicentry",enable_events=True)], [gui.Text(text="Question (Leave Blank For Whole Topic Deletion",key="questiontext")],[gui.Input("",key="questionentry",enable_events=True)],[gui.Button("Delete Card/Topic")]]
            cardwindow = gui.Window("Revision Helper : Card Deleter",layout=cardlayout,margins=(0,0),resizable=False)
            cardwindow.read()
            while True:
                event, values = cardwindow.read()
                if event in (None,"Cancel"):
                    break
                elif event in ("Delete Card/Topic"):
                    if (cardwindow["topicentry"].get()).strip() !="":
                        if cardwindow["questionentry"].get().strip() == "":
                            for i in os.listdir("Cards/"+currentsubject+"/"+cardwindow["topicentry"].get()+"/"):
                                os.remove("Cards/"+currentsubject+"/"+cardwindow["topicentry"].get()+"/"+i)
                            os.rmdir("Cards/"+currentsubject+"/"+cardwindow["topicentry"].get()+"/")
                        else:
                            os.remove("Cards/"+currentsubject+"/"+cardwindow["topicentry"].get()+"/"+cardwindow["questionentry"].get())
                            if len(os.listdir("Cards/"+currentsubject+"/"+cardwindow["topicentry"].get()+"/")) == 0:
                                os.rmdir("Cards/"+currentsubject+"/"+cardwindow["topicentry"].get()+"/")
                        UpdateTree()
                        break
                    else:
                        gui.popup_error("Enter At Least The Topic")
            cardwindow.close()
        else:
            gui.popup_error("Choose A Subject First")
