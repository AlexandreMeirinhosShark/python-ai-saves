import pyautogui as gui
import tkinter.messagebox as msg
import tkinter as tk

TECLAS = []

def keypos(event):
    global TECLAS
    if event.keysim == "f":
        x, y = gui.position()
        TECLAS.append((x, y))
    print(TECLAS)


ask = msg.askokcancel("~Posição do rato", "É preciso definir a posição das áreas de clique antes de começar.\nPrima F para marcar uma posição.")

root = tk.Tk()
root.geometry("200x200")
root.title("AAAAA")
root.bind("<Key>", keypos)

root.mainloop()