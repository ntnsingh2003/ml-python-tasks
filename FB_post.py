import pyautogui
import time
import os
import pygetwindow as gw

pyautogui.FAILSAFE = True

# Step 1: Open Facebook App
app_id = "Chrome._crx_kippjgbkgbpmgej.UserData.Profile4"  
os.system(f'explorer shell:AppsFolder\\{app_id}')
time.sleep(2)

# Step 2: Activate Facebook window
windows = gw.getWindowsWithTitle("Facebook")  # Replace "X" if Facebook has a different title
if not windows:
    print("❌ Facebook window not found.")
    exit()

Facebook_win = windows[0]
Facebook_win.activate()
Facebook_win.maximize()
print("✅ Facebook window activated.")
time.sleep(1)

# Step 3: Click on 'Create Post' area
print("Clicking Facebook post box...")
pyautogui.click(x=740, y=165)  # 🔧 Adjust if necessary
time.sleep(1)

# Step 4: Write the message
print("Typing Facebook post...")
pyautogui.write("Automated FB Message using Python without any API integration", interval=0.05)
time.sleep(2)

# Step 5: Locate and click 'Post' button using image
print("Locating Post button...")
post_location = pyautogui.locateCenterOnScreen(r"C:\Users\nitin\Downloads\ml\Task\FBpostButton.png", confidence=0.6)

if post_location:
    print(f"✅ Found Post button at {post_location}, clicking...")
    pyautogui.click(post_location)
    print("✅ Facebook post sent!")
else:
    print("❌ Could not find Post button. Please check your screenshot or screen resolution.")
