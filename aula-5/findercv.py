import tkinter as tk
import pyautogui as gui

root=tk.Tk()
root.title("FinderCV")
root.geometry("500x700")
root.wm_resizable(False, False)

title=tk.Label(font="Aptos 30 bold", text="Finder CV", width=14, bg="#dddddd")
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

root.mainloop()