import tkinter as tk
from tkinter import filedialog
import webbrowser
import pyautogui as gui
import os
file_path = ""
# This is a program that, when selecting a file or taking a screenshot, will open obamify.com.
# The user can then upload the file manually.

class Snipper:
    def __init__(self, root):
        self.root = root
        self.start_x = None
        self.start_y = None
        self.current_rect = None
        
        # Transparent window for selection
        self.snip_window = tk.Toplevel(root)
        self.snip_window.attributes("-fullscreen", True)
        self.snip_window.attributes("-alpha", 0.3)
        self.snip_window.configure(bg='black')
        self.snip_window.bind("<ButtonPress-1>", self.on_press)
        self.snip_window.bind("<B1-Motion>", self.on_drag)
        self.snip_window.bind("<ButtonRelease-1>", self.on_release)
        self.snip_window.bind("<Escape>", lambda e: self.snip_window.destroy())
        
        self.canvas = tk.Canvas(self.snip_window, cursor="cross", bg="grey11")
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def on_press(self, event):
        self.start_x = self.canvas.canvasx(event.x)
        self.start_y = self.canvas.canvasy(event.y)
        self.current_rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_drag(self, event):
        cur_x = self.canvas.canvasx(event.x)
        cur_y = self.canvas.canvasy(event.y)
        self.canvas.coords(self.current_rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_release(self, event):
        end_x = self.canvas.canvasx(event.x)
        end_y = self.canvas.canvasy(event.y)
        self.snip_window.destroy()
        
        # Calculate coordinates for pyautogui
        x = min(self.start_x, end_x)
        y = min(self.start_y, end_y)
        width = abs(end_x - self.start_x)
        height = abs(end_y - self.start_y)
        
        if width > 0 and height > 0:
            take_screenshot(region=(int(x), int(y), int(width), int(height)))

def automate(filepath):
    print(filepath)
    for i in range(5):
        gui.press("tab", interval=0.1)
    gui.press("enter", interval=2)
    gui.write(filepath, interval=0.05)
    gui.press("enter", interval=0.5)
    gui.click(root.winfo_screenwidth() / 2, root.winfo_screenheight() / 2 - 100)
    gui.press("tab")
    gui.press("tab")
    gui.press("enter", interval=0.1)
    for i in range(26):
        gui.press("tab", interval=0.1)
    gui.press("enter", interval=0.1)

def open_obamify():
    global file_path
    webbrowser.open("https://obamify.com/")
    root.after(10000, lambda: automate(file_path))

def select_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")])
    if file_path:
        print(f"Selected file: {file_path}")
        open_obamify()

def start_snip(event=None):
    root.withdraw() # Hide main window during snip
    Snipper(root)
    # Note: We need to show the window again after snipping, 
    # but since Snipper destroys its own window, we can just deiconify root in take_screenshot or keep it simple.
    # For now, let's just schedule root to reappear after a delay or let the Snipper callback handle it.
    # Actually, simpler: just wait for the user to interact.
    pass

def take_screenshot(region=None):
    global file_path
    # region argument matches pyautogui.screenshot expectation (left, top, width, height)
    if region:
        screenshot = gui.screenshot(region=region)
    else:
        screenshot = gui.screenshot()
    
    filename = "screenshot.png"
    file_path = os.path.abspath(filename)
    screenshot.save(file_path)
    print(f"Screenshot saved to: {file_path}")
    
    root.deiconify() # Bring main window back
    open_obamify()

root = tk.Tk()
root.title("Auto Obamify")
root.geometry("400x300")

# Instruction label
instruction_text = (
    "Click 'Select File' to choose an image,\n"
    "or press 'F' (or click 'Take Screenshot') to capture a screen region.\n"
    "The image will be saved and Obamify.com will open."
)
label = tk.Label(root, text=instruction_text, padx=20, pady=20)
label.pack()

btn_file = tk.Button(root, text="Select File", command=select_file, height=2, width=20)
btn_file.pack(pady=10)

btn_snip = tk.Button(root, text="Take Screenshot", command=lambda: start_snip(), height=2, width=20)
btn_snip.pack(pady=10)

root.bind("<f>", start_snip)
root.bind("<F>", start_snip) # Handle shift+f too

root.mainloop()

