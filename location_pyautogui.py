import pyautogui

# Move the mouse to some random position before getting the current position
pyautogui.moveTo(100, 100, duration=0.5)

mouse_x, mouse_y = pyautogui.position()
print(f"Mouse Position: ({mouse_x}, {mouse_y}) pixels")
while True:
    print(pyautogui.position())