import tkinter as tk
import pyautogui as gui
from datetime import datetime as date

def captura():
    nam = entry.get()
    tst = date.now().strftime("%Y%m%d_%H%M%S")
    gui.hotkey("alt", "space")
    gui.write("n\n", interval=0.2)
    img = gui.screenshot()
    img.save(f"{nam}{tst}.png")

#main window
root = tk.Tk()
root.title("Print Screen")
root.wm_resizable(False, False)
root.geometry("300x300")

#rest
tk.Label(text="Captura de Ecrã", font="tkDefaultFont 18 bold").pack(pady=20)
entry = tk.Entry(width=12, text="Entre seu texto.", font="tkDefaultFont 18", bg="#dddddd")
entry.pack(pady=20)
lbl = tk.Button(width=15, height=3, text="Capturar", bg="#cccccc", command=captura)
lbl.pack(pady=20)

root.mainloop()