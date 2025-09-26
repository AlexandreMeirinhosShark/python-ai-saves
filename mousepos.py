import tkinter as tk
import pyautogui

def update_position():
    x, y = pyautogui.position()
    position_label.config(text=f"Global mouse position: x={x}, y={y}")
    root.after(50, update_position)  # Update every 50 milliseconds

def toggle_fullscreen():
    global fullscreen
    fullscreen = not fullscreen
    root.attributes("-fullscreen", fullscreen)

root = tk.Tk()
root.title("Global Mouse Position Tracker")

fullscreen = False

position_label = tk.Label(root, text="Tracking global mouse position...", font=("Arial", 16))
position_label.pack(padx=20, pady=20)

fullscreen_button = tk.Button(root, text="Toggle Fullscreen", command=toggle_fullscreen)
fullscreen_button.pack(pady=10)

update_position()  # Start updating the position
root.mainloop()