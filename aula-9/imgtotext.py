import cv2
import pytesseract
import tkinter as tk
from tkinter import filedialog

path = None # global path variable to store selected file path

def itt():
    global path
    path = pick_file()
    if not path:
        return
    img = cv2.imread(path)

    trs = pytesseract.image_to_string(img)
    lbl.config(text=trs)

def pick_file():
    filepath = filedialog.askopenfilename(
        title="Tkinter",
        filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp"),]
    )
    
    if filepath:  # user did not cancel
        return filepath
    else:
        return None

root = tk.Tk()
root.geometry("500x500")
root.title("Imagem para Texto")
root.wm_resizable(False, False)
root.config(bg="light grey")

titl = tk.Label(root, font="Arial 18 bold", text="»Image to Text«", bg="light grey")
titl.pack(pady=10)
lbl = tk.Label(root, width=50, height=20, font="Arial 10", relief="sunken", bg="white", text="Pick an image to process it into text!\n\n:D", wraplength=400, anchor="nw", justify="left")
lbl.pack(pady=20)
btn = tk.Button(root, font="Arial 12 bold", text="Search Image", bg="navy", fg="white", command=itt)
btn.place(x=200, y=450)

root.mainloop()
