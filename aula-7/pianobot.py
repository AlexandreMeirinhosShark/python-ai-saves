import pyautogui as gui
import tkinter.messagebox as msg
import tkinter as tk
from tkinter import font

TECLAS = [None, None, None, None]

select = [1, 2, 3, 4]


def keypos(event):
    global TECLAS, select
    x, y = gui.position()
    TECLAS[seon.get()-1] = (x, y)
    msg.showinfo(None, f"Posição {seon.get()} adquirida: {x, y}")

def ready():
    global TECLAS
    if None in TECLAS:
        msg.showwarning("Aviso", "Nem todas as posições foram marcadas.\nTente novamente.")
    else:
        aks = msg.askyesnocancel("Começar", "Se quiser o FNF, clique Sim, se não clique Não para configurar para piano.")

ask = msg.askokcancel("~Posição do rato", "É preciso definir a posição das áreas de clique antes de começar.\nPrima F para marcar uma posição.")

root = tk.Tk()
seon = tk.IntVar()
seon.set(1)
root.geometry("300x300")
root.title("PianoBot")
root.bind("<f>", keypos)

lbl = tk.Label(text="Posições:", font="Arial 17 bold")
lbl.place(x=10, y=198)
ittle = tk.Label(text="-»)PianoBot(«-", font="Arial 20 bold")
ittle.pack(pady=20)
btn = tk.Button(font="Arial 14 bold", command=ready, text="~Começar~")
btn.pack(pady=50)
ddn = tk.OptionMenu(root, seon, *select)
ddn.place(x=200, y=200)
ddn["menu"].config(font="Arial 18 bold")

root.mainloop()

