import cv2
import pytesseract as tess
import tkinter as tk
from tkinter import filedialog

def itt():
    img = cv2.imread(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # tess.image_to_string(gray)

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

titl = tk.Label(root, font="Arial 18 bold", text="»Image to Text«")
titl.pack(pady=10)
lbl = tk.Label(root, width=20, height=10, font="Arial 18", relief="sunken", bg="white", text="Nothing.")
lbl.pack(pady=90)

root.mainloop()