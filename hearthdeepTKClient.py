#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.filedialog import *
from requests.auth import HTTPBasicAuth
import requests
import fileinput
import sys,os

def alert():
    showinfo("alerte", "Bravo!")

def update_status():
    current_status = message.get()
    if current_status.endswith("..."):
        message.set("Waiting")
        fenetre.after(1000,update_status)
    elif current_status.startswith("Waiting"):
        current_status += '.'
        message.set(current_status)
        fenetre.after(1000,update_status)

def stop():
    message.set('STOP')

def clickLogin():
    toplevel = Toplevel()
    toplevel.title("Login")
    toplevel.maxsize(200,75)
    entry_user = Entry(toplevel, textvariable=username, width=100)
    entry_user.pack()
    entry_pass = Entry(toplevel, textvariable=password, width=100 , show="*")
    entry_pass.pack()
    button = Button(toplevel, text="Connection ...",command= lambda: clickLoginOut(toplevel,entry_user,entry_pass), width=100)
    button.pack()

def clickLoginOut(window,username,password):
    #some stuff
    print(username.get(),password.get())
    res = requests.get('http://hearthdeep.lirmm.fr/api/hearthlog/', auth=HTTPBasicAuth(username.get(), password.get()))
    print(res.status_code)
    if(res.status_code == 200):
        resjson = res.json()
        for js in resjson:
            listupload.append(js['filename'])
        connect.set(True)
        fenetre.title(username.get())
        message.set('Wellcome '+username.get()+"!")
        print(listupload)
    else:
        connect.set(False)
        fenetre.title("HearthDeepClient")
        message.set('Login error ...')
    print(connect.get())

    window.destroy()

def clickConfig():
    dirname = askdirectory(title="Fichier log.config ")
    message.set(dirname)
    if(dirname):
        listFileRep = os.listdir(dirname)
        checkList = ['Logs','Cache','options.txt']
        if(set(checkList)<set(listFileRep)):
            rewrite_logconfig(path+'/log.config')
            setConfigClient('LogsPath',path+'/Logs/')
            logs_path.set(path+'/Logs/')
            message.set("Config match and rewrite")
        else:
            message.set("Bad setting repository")

def rewrite_logconfig(filename):
    logFile = open('config/log.config','r')
    orgLogFile = open(filename,'w')
    orgLogFile.write(logFile.read())

def setConfigClient(champs, valeur):
    for line in fileinput.input('config/hearthdeep.config', inplace=True):
        if champs in line:
            line = champs+':'+valeur
        sys.stdout.write(line)

fenetre = Tk()
fenetre.title("HearthDeepClient")
fenetre.maxsize(350,125)
fenetre.minsize(350,125)


message = StringVar()
message.set('Waiting')


username = StringVar()
password = StringVar()
username.set("Username")
password.set("Password")

connect = BooleanVar()
connect.set(False)
listupload=[]
state = StringVar()
state.set("Offline...")
logs_path = StringVar()

menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Login", command=clickLogin)
menu1.add_separator()
menu1.add_command(label="Quitter", command=fenetre.quit)
menubar.add_cascade(label="Paramaters", menu=menu1)


labelFrame = LabelFrame(fenetre, text="Informations",width=300, height=50)
labelFrame.pack(side=LEFT, padx=5, pady=5, fill="both", expand="yes")
label = Label(labelFrame,textvariable=message).pack(side=LEFT)
Button(fenetre, text ='Configuration',command=clickConfig).pack(side=TOP, padx=5, pady=5)
Button(fenetre, textvariable=state,command=stop).pack(side=BOTTOM, padx=5, pady=5)


# Canvas(fenetre, width=250, height=50, bg='grey').pack(side=LEFT, padx=5, pady=5)

fenetre.config(menu=menubar)

update_status()

fenetre.mainloop()
