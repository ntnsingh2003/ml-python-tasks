import pyautogui
import time
import os
import pygetwindow as gw

pyautogui.FAILSAFE = True


print("Opening LinkedIN App...")
app_id = ""
os.system(f'explorer shell:AppsFolder\\{app_id}')
time.sleep(5)


windows = gw.getWindowsWithTitle("LinkedIn")
if not windows:
    print(" LinkedIn window not found.")
    exit()
linkedin_win = windows[0]
linkedin_win.activate()
linkedin_win.maximize()
print(" LinkedIn window activated.")
time.sleep(2)


print("Clicking 'Create a Post' button...")
pyautogui.click(x=694, y=168)
time.sleep(5)


message = "Hello LinkedIn! Automated post using Python & pyautogui "
print("Typing post...")
pyautogui.write(message, interval=0.05)


print("Clicking Post...")
time.sleep(2)
pyautogui.click(x=1355, y=787)  # Adjust if necessary
time.sleep(2)

print(" Post successfully made!")
