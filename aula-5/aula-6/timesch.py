import tkinter as tk
import sys
from tkinter import messagebox as msg
try:
    import pyautogui as gui
except ModuleNotFoundError:
    print("PyAutoGUI não está instalado. Instala através de ''pip install pyautogui''.")
    msg.showerror("Biblioteca não encontrada", "PyAutoGUI não está instalado. Instala através de ''pip install pyautogui''.")
    sys.exit(0)
from time import sleep
from datetime import datetime as date
import os
import subprocess as subp

#functions
def screen():
    try:
        yres = int(resent2.get())
        xres = int(resent.get())
        tst = date.now().strftime("%Y%m%d_%H%M%S")
    except ValueError:
        msg.showwarning("Aviso:", "Os valores de resolução da captura têm de ser números. Tenta novamente.")
        return
    root.iconify()
    sleep(1)
    #folder stuff
    script_dir = os.path.dirname(os.path.abspath(__file__))
    folder = os.path.join(script_dir, "Screenshots")
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, f"screenshot{tst}.png")
    #folder stuff end
    try:
        img = gui.screenshot(region=(0, 0, xres, yres))
        img.save(filepath)
        chec = msg.askyesno("Salvo!", "A captura de ecrã foi salva na pasta ''Screenshots''. Queres vê-la?")
        if chec:
            subp.Popen(f'explorer "{folder}"')
    except Exception:
        msg.showerror("Erro de PyAutoGUI", "PyAutoGUI não conseguiu importar PyScreeze. Verifica se ''pillow'' está instalado no teu Python.")
    root.deiconify()

def screenm(vr):

    try:
        yres = int(resent2.get())
        xres = int(resent.get())
        tst = date.now().strftime("%Y%m%d_%H%M%S")
        secs = float(intent.get())
    except ValueError:
        msg.showwarning("Aviso:", "Os valores da captura têm de ser números. Tenta novamente.")
        return
    
    if root.state() == "iconic":
        script_dir = os.path.dirname(os.path.abspath(__file__))
        folder = os.path.join(script_dir, "VidScreenshots")
        os.makedirs(folder, exist_ok=True)
        filepath = os.path.join(folder, f"screenshot{tst}.png")
        try:
            img = gui.screenshot(region=(0, 0, xres, yres))
            img.save(filepath)
            
        except Exception:
            msg.showerror("Erro de PyAutoGUI", "PyAutoGUI não conseguiu importar PyScreeze. Verifica se ''pillow'' está instalado no teu Python.")
    else:
        root.iconify()
    if vr != 0:
        root.after(int(secs*1000), screenm, vr-1)
    else:
        root.deiconify()
        chec = msg.askyesno("Salvo!", "A captura de ecrã foi salva na pasta ''VidScreenshots''. Queres vê-la?")
        if chec:
            subp.Popen(f'explorer "{folder}"')
        return

root=tk.Tk()
root.title("TimeSCH")
root.geometry("340x420")
root.config(bg="white")
root.wm_resizable(False, False)

#labels:
    #cosmetic
sclbl=tk.Label(root, text="Captura Única", bg="#4086f7", font="Aptos 18 bold", fg="white", width=25, height=1)
sclbl.pack()
loplbl=tk.Label(root, text="Captura Repetida", bg="#4086f7", font="Aptos 18 bold", fg="white", width=25, height=1)
loplbl.pack(pady=170)
    #useful
reslbl=tk.Label(root, text="Resolução:", font="Aptos 14 bold", bg="white")
reslbl.place(x=10, y=80)
lplbl=tk.Label(root, text="Repetir:", font="Aptos 14 bold", bg="white")
lplbl.place(x=10, y=270)
intlbl=tk.Label(root, text="Intervalo:", font="Aptos 14 bold", bg="white")
intlbl.place(x=10, y=320)
multiplication=tk.Label(root, text="*", font="Aptos 22 bold", bg="white", fg="#306bc9")
multiplication.place(x=190, y=80)

#entries:
    #single screenshot
resent=tk.Entry(root, font="Aptos 12", highlightthickness=2, bd=0, highlightbackground="black", width=6)
resent.place(x=125, y=82)
resent2=tk.Entry(root, font="Aptos 12", highlightthickness=2, bd=0, highlightbackground="black", width=6)
resent2.place(x=210, y=82)
    #looped screenshot
repent=tk.Entry(root, font="Aptos 12", highlightthickness=2, bd=0, highlightbackground="black", width=6)
repent.place(x=140, y=272)
intent=tk.Entry(root, font="Aptos 12", highlightthickness=2, bd=0, highlightbackground="black", width=6)
intent.place(x=140, y=322)

#buttons
scbtn=tk.Button(root, font="Aptos 12 bold", bd=3, bg="#0e64ed", fg="white", width=11, text="Capturar", command=screen)
scbtn.place(x=110, y=140)
lopbtn=tk.Button(root, font="Aptos 12 bold", bd=3, bg="#0e64ed", fg="white", width=11, text="Começar", command=lambda: screenm(int(repent.get())))
lopbtn.place(x=110, y=370)

root.mainloop()