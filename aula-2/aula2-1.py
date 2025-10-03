import pyautogui as gui
from time import sleep

gui.press("win")
sleep(.5)
gui.write("paint")
sleep(.5)
gui.press("enter")
sleep(1)
for i in range(17):
    gui.press("tab")
gui.press("enter")
sleep(1)
for i in range(2):
    gui.press("right")
gui.press("enter")
gui.moveTo(750, 513, duration=0.7)
gui.click(interval=0.5)
gui.dragRel(250, 250, duration=1)
gui.moveRel(50, 50, duration=0.5)
gui.click()
gui.press("b")
for i in range(27):
    gui.press("tab")
for i in range(3):
    gui.press("right")
gui.press("enter")
gui.move(-150, -150, duration=1)
gui.click()
sleep(5)
gui.hotkey("alt", "f4", interval=0.5)
gui.press("n")