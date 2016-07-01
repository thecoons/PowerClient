#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.filedialog import *
from requests.auth import HTTPBasicAuth
import requests
import fileinput
import sys, os
import time

#Waiting animation
def update_status():
    current_status = message.get()
    if current_status.endswith("..."):
        message.set("Waiting")
        fenetre.after(1000,update_status)
    elif current_status.startswith("Waiting"):
        current_status += '.'
        message.set(current_status)
        fenetre.after(1000,update_status)

#Event login
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
#Event "connect"
def clickLoginOut(window,username,password):
    print(username.get(),password.get())
    res = requests.get('http://hearthdeep.lirmm.fr/api/hearthlog/', auth=HTTPBasicAuth(username.get(), password.get()))
    print(res.status_code)
    if(res.status_code == 200):
        resjson = res.json()
        for js in resjson:
            listupload.append(js['filename'])
        connect.set(True)
        fenetre.title(username.get())
        loadConfig()
        print(listupload,logs_path.get())
    else:
        connect.set(False)
        fenetre.title("HearthDeepClient")
        message.set('Login error ...')
    print(connect.get())
    window.destroy()
#Check if ready to start
def ready(power_button):
    if(connect.get() and logs_path.get()):
        message.set('Ready to start !!!')
        power_button.config(state="normal")
    elif(not connect.get()):
        message.set('You have to sign in...')
        power_button.config(state="disable")
    else:
        message.set('Set the log.config directory.')
        power_button.config(state="disable")


#Event Config
def clickConfig():
    dirname = askdirectory(title="Fichier log.config ")
    if(dirname):
        listFileRep = os.listdir(dirname)
        checkList = ['Logs','Cache','options.txt']
        if(set(checkList)<set(listFileRep)):
            rewrite_logconfig(dirname+'/log.config')
            setConfigClient('LogsPath',dirname+'/Logs/')
            logs_path.set(dirname+'/Logs/')
            message.set("Config match and rewrite. RDY!")
        else:
            message.set("Bad setting repository")
#Event Lunch
def clickLunch(list_upload):
    if(not power.get()):
        power.set(True)
        state.set("Online!")
        check_send(list_upload)
    else:
        power.set(False)
        state.set("Offline...")
        message.set("Waiting")
        update_status()

#Hearthstone's log sniffing
def check_send(list_upload):
    print("ClickLunch Call...")
    list_in_rep = os.listdir(logs_path.get())
    gen = [line for line in list_in_rep if line not in list_upload]
    for line in gen:
        last_touch = os.path.getmtime(logs_path.get()+line)
        current_time = time.time()
        inter_time = current_time - last_touch
        print('ClickLunch Call: '+line+' '+str(last_touch)+' '+str(current_time)+' '+str(inter_time))
        if(inter_time > 30000):
            send_log(line)
            list_upload.append(line)

    if not gen:
        message.set('Nothing to send... yet')

    if(power):
        fenetre.after(1000*60,lambda : check_send(list_upload))
#Envoie du fichier de log Hearthstone
def send_log(filename):
        files = {'brutLog': open(logs_path.get()+filename, 'rb')}
        res = requests.post('http://hearthdeep.lirmm.fr/api/hearthlog/', files=files,data={'filename':filename}, auth=HTTPBasicAuth(username.get(), password.get()))
        print('SendLog: status_code req :'+ str(res.status_code))

        if(res.status_code == 201):
            message.set("Successful logs send !")
        else:
            message.set("Fail to send logs ...")
#Rewrite log.config
def rewrite_logconfig(filename):
    logFile = open('config/log.config','r')
    orgLogFile = open(filename,'w')
    orgLogFile.write(logFile.read())
#Set the client config file
def setConfigClient(champs, valeur):
    for line in fileinput.input('config/hearthdeep.config', inplace=True):
        if champs in line:
            line = champs+':'+valeur
        sys.stdout.write(line)
#Charger le ficheir de config
def loadConfig():
        f = open('config/hearthdeep.config','r')
        match = re.match(r'^LogsPath:(.*)', f.read())
        logs_path.set(match.group(1))

#Main Window
fenetre = Tk()
fenetre.title("HearthDeepClient")
fenetre.maxsize(350,125)
fenetre.minsize(350,125)
#Information Message
message = StringVar()
message.set('Waiting')
#Username
username = StringVar()
username.set("Username")
#User's Password
password = StringVar()
password.set("Password")
#User is connect ?
connect = BooleanVar()
connect.set(False)
#File already upload
listupload=[]
#Label of activate sniffing
state = StringVar()
state.set("Offline...")
#Path to log.config
logs_path = StringVar()
# logs_path.trace("w",ready)
#The client is active?
power = BooleanVar()
power.set(False)
#Menu Bar
menubar = Menu(fenetre)
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Path Configuration", command=clickConfig)
menu1.add_separator()
menu1.add_command(label="Quit", command=fenetre.quit)
menubar.add_cascade(label="Paramaters", menu=menu1)
fenetre.config(menu=menubar)
#Button rigth side
labelFrame = LabelFrame(fenetre, text="Informations",width=300, height=50)
labelFrame.pack(side=LEFT, padx=5, pady=5, fill="both", expand="yes")
label = Label(labelFrame,textvariable=message).pack(side=LEFT)
Button(fenetre, text ='Login',command=clickLogin).pack(side=TOP, padx=5, pady=5)
power_button = Button(fenetre, state="disable",textvariable=state,command=lambda : clickLunch(listupload))
power_button.pack(side=BOTTOM, padx=5, pady=5)
#Trace conect
connect.trace("w",lambda a,b,c,x=power_button : ready(x))
logs_path.trace("w",lambda a,b,c,x=power_button : ready(x))
#Seed animation
update_status()
#Loop the app
fenetre.mainloop()
