#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *

fenetre = Tk()
fenetre.title("HearthDeepClient")

def alert():
    showinfo("alerte", "Bravo!")

menubar = Menu(fenetre)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Créer", command=alert)
menu1.add_separator()
menu1.add_command(label="Quitter", command=fenetre.quit)
menubar.add_cascade(label="Connect", menu=menu1)

fenetre.config(menu=menubar)

l = LabelFrame(fenetre, text="Informations",width=250, height=50).pack(side=LEFT, padx=5, pady=5)

# Label(l, text="A l'intérieure de la frame").pack()
# Canvas(fenetre, width=250, height=50, bg='grey').pack(side=LEFT, padx=5, pady=5)
Button(fenetre, text ='Configuration').pack(side=TOP, padx=5, pady=5)
Button(fenetre, text ='Enable/Disable').pack(side=BOTTOM, padx=5, pady=5)

fenetre.mainloop()
