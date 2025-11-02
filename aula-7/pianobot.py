import pyautogui as gui
import tkinter.messagebox as msg
import tkinter as tk
from tkinter import font
import time

POS = [None, None, None, None]

select = [1, 2, 3, 4]

pressed_keys = {None}

stopped = False


def friday():
    global POS, stopped, pressed_keys

    # Remove placeholder if still present
    if None in pressed_keys:
        pressed_keys.remove(None)

    if stopped:
        print("stopped")
        # Release any held keys when stopping
        for key in pressed_keys:
            gui.keyUp(key)
        pressed_keys.clear()
        stopped = False
        return

    # Color-to-key mapping (same as before)
    color_map = {
        (194, 75, 153): "left",
        (0, 255, 255): "down",
        (18, 250, 5): "up",
        (249, 57, 63): "right",
    }

    # Take one screenshot for efficiency
    screenshot = gui.screenshot()

    # Detect which keys should be active this frame
    detected_keys = {None}
    for pos in POS:
        col = screenshot.getpixel(pos)
        if col in color_map:
            detected_keys.add(color_map[col])

    if None in detected_keys:
        detected_keys.remove(None)

    # --- HOLD UNTIL NEXT KEY LOGIC ---

    # Only act when a *new* key (or key set) appears
    if detected_keys != pressed_keys:
        # Release all previously held keys
        for key in pressed_keys:
            gui.keyUp(key)
        # Press all new keys
        for key in detected_keys:
            gui.keyDown(key)
        # Update current state
        pressed_keys = detected_keys

    # Repeat quickly
    root.after(10, friday)

def piano(ifsa=0):
    global POS, stopped
    sarf = 0
    if stopped:
        print("stopped")
        stopped = False
        return
    else:
        for i in range(4):
            col = gui.pixel(*POS[i])
            if col == (0, 0, 0):
                gui.click(POS[i][0], POS[i][1]+int(ifsa))
                if sarf < 10:
                    sarf = 0.2
        root.after(10, piano, ifsa + sarf)

def keypos(event):
    global POS, select
    x, y = gui.position()
    POS[seon.get()-1] = (x, y)
    msg.showinfo(None, f"Posição {seon.get()} adquirida: {x, y}")

def ready():
    global POS, stopped
    if None in POS:
        msg.showwarning("Aviso", "Nem todas as posições foram marcadas.\nTente novamente.")
    else:
        stopped = False
        aks = msg.askyesnocancel("Começar", "Se quiser o FNF, clique Sim. Se não, clique Não para configurar para piano.\nMove o rato para parar.")
        if aks == None:
            print("canceled")
            return
        elif aks:
            print("fnf")
            root.iconify()
            friday()
        else:
            print("piano")
            root.iconify()
            piano()

ask = msg.askokcancel("~Posição do rato", "É preciso definir a posição das áreas de clique antes de começar.\nPrima F para marcar uma posição.")

root = tk.Tk()
seon = tk.IntVar()
seon.set(1)
root.geometry("300x300")
root.title("PianoBot")
root.bind("<f>", keypos)
root.bind("<t>", lambda: globals().__setitem__("stopped", True))

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


