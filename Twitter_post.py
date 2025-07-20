import pyautogui
import time
import os
import pygetwindow as gw

pyautogui.FAILSAFE = True

# Step 1: Open Twitter App
app_id = "Chrome._crx_lodlkfgiljnadcf.UserData.Profile4"
os.system(f'explorer shell:AppsFolder\\{app_id}')
time.sleep(4)

# Step 2: Activate Twitter window
windows = gw.getWindowsWithTitle("X")
if not windows:
    exit()
x_win = windows[0]
x_win.activate()
x_win.maximize()
time.sleep(2)

# Step 3: Click on 'Create Post' area
pyautogui.click(x=736, y=152)  # Adjust these
time.sleep(2)

# Step 4: Write tweet
pyautogui.write("Automated Tweet using Python Script without any help of API", interval=0.05)

# Step 5: Post the tweet
time.sleep(1)
pyautogui.hotkey('ctrl', 'enter')  # Try post
time.sleep(2)

'''
#2nd Method Using Browser
import webbrowser
import pyautogui
import time
webbrowser.open("https://twitter.com/compose/tweet")
time.sleep(5)
pyautogui.write("Tweet via browser ✨", interval=0.05)
pyautogui.hotkey('ctrl', 'enter')  # Works great in browser

'''