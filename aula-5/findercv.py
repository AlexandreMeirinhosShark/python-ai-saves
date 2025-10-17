import tkinter as tk
import pyautogui as gui
from platform import system
from tkinter import messagebox as msg
from time import sleep

#functions
def websearch():
    name = name_ent.get()
    num = num_ent.get()
    adres = ad_ent.get()
    if system() == "Windows":
        gui.press("win", interval=1)
        gui.write("edge\n", interval=0.05)
        sleep(5)
        if num.isdigit():
            gui.write("https://www.ligaram-me.pt \n", interval=0.05)
            for i in range(5):
                gui.press("tab", interval=0.05)
            gui.write(f"{num}\n", interval=0.05)
        else:
            msg.showerror("Erro", "A entrada do seu número só pode ter o seu número.\nVerifique se existem espacos ou qualquer outro carater que não sejam algarismos.")
            return
        #
    elif system() == "Darwin":
        gui.hotkey("cmd", "space", interval=1)
        gui.write("Safari\n")
        msg.showinfo("Unfinished", "Project is still in alpha.")
        #gui.hotkey("cmd", "q")
    elif system() == "Linux":
        gui.hotkey('ctrl', 'alt', 't', interval=1)
        gui.write('firefox\n', interval=0.05)
        msg.showinfo("Unfinished", "Project is still in alpha.")
        #gui.hotkey("alt", "f4")

#main window
root=tk.Tk()
root.title("Finder CV")
root.geometry("500x700")
root.wm_resizable(False, False)

title=tk.Label(font="Aptos 30 bold", text="Finder CV", width=20, bg="#dddddd")
title.pack()
#entries
name_ent=tk.Entry(root, font="Aptos 14", highlightthickness=2, bd=0, highlightbackground="black")
name_ent.place(x=150, y=100)
ad_ent=tk.Entry(root, font="Aptos 14", highlightthickness=2, bd=0, highlightbackground="black")
ad_ent.place(x=150, y=170)
num_ent=tk.Entry(root, font="Aptos 14", highlightthickness=2, bd=0, highlightbackground="black")
num_ent.place(x=150, y=240)
#labels
namelbl=tk.Label(root, font="Aptos 15", text="Nome:")
namelbl.place(x=10, y=100)
adlbl=tk.Label(root, font="Aptos 15", text="Endereço:")
adlbl.place(x=10, y=170)
numlbl=tk.Label(root, font="Aptos 15", text="Número:")
numlbl.place(x=10, y=240)
#buttons
webbtn=tk.Button(root, font="Aptos 15 bold", text="PESQUISA WEB", width=15,
height=3, bd=4, relief="solid", bg="magenta", command=websearch)
webbtn.place(x=200, y=500)

root.mainloop()
adlbl.place(x=10, y=170)
numlbl=tk.Label(root, font="Aptos 15", text="Número:")
numlbl.place(x=10, y=240)


root.mainloop()
