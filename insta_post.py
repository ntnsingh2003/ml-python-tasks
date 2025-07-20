import pyautogui
import time
import os
import pygetwindow as gw
from datetime import datetime

pyautogui.FAILSAFE = True

def find_and_click(image, x, y, confidence=0.8):
    """Helper function to find image or use fallback coordinates"""
    try:
        btn = pyautogui.locateCenterOnScreen(image, confidence=confidence)
        pyautogui.click(btn)
        return btn
    except:
        pyautogui.click(x, y)
        return None

def instagram_post(image_path, caption):
    # Step 1: Open Instagram App (Chrome App)
    app_id = "Chrome._crx_akpamldlcfphjmp.UserData.Profile4"  
    os.system(f'explorer shell:AppsFolder\\{app_id}')
    time.sleep(3)

    # Step 2: Activate Instagram window
    windows = gw.getWindowsWithTitle("Instagram")  # Adjust title if needed
    if not windows:
        print("❌ Instagram window not found.")
        return

    Instagram_win = windows[0]
    Instagram_win.maximize()
    print("✅ Instagram window activated.")
    time.sleep(3)

    # Step 3: Click Create button (plus icon)
    print("Clicking Create button...")
    try:
        create_btn = pyautogui.locateCenterOnScreen(r"C:\Users\nitin\Downloads\ml\Task\create_button.png", confidence=0.8)
        pyautogui.click(create_btn)
    except:
        pyautogui.click(x=100, y=726)  # Manual fallback (adjust as needed)
    time.sleep(2)

    # Step 4: Select "Post" option
    print("Selecting Post option...")
    try:
        post_option = pyautogui.locateCenterOnScreen(r"C:\Users\nitin\Downloads\ml\Task\post_option.png", confidence=0.8)
        pyautogui.click(post_option)
    except:
        pyautogui.click(x=87, y=795)  # Manual fallback
    time.sleep(2)

    # Step 5: Select from computer
    print("Opening file dialog...")
    try:
        select_from_computer = pyautogui.locateCenterOnScreen(r"C:\Users\nitin\Downloads\ml\Task\select_computer.png", confidence=0.8)
        pyautogui.click(select_from_computer)
    except:
        pyautogui.hotkey('ctrl', 'shift', 'g')  # Chrome file dialog shortcut
    time.sleep(1)

    # Step 6: Enter file path and press Enter
    pyautogui.write(image_path)
    pyautogui.press('enter')
    time.sleep(3)

    # Step 7: First Next button
    print("Clicking Next...")
    find_and_click(r"C:\Users\nitin\Downloads\ml\Task\next_button.png", x=1210, y=285)
    time.sleep(2)

    # Step 8: Second Next button
    print("Clicking Next again...")
    find_and_click(r"C:\Users\nitin\Downloads\ml\Task\next_button.png", x=1426, y=286)
    time.sleep(2)

    # Step 9: Write caption
    print("Writing caption...")
    find_and_click(r"C:\Users\Acer\Desktop\Tasks\Py\caption_box.png", x=1110, y=418)
    pyautogui.write(caption, interval=0.05)
    time.sleep(1)

    # Step 10: Click Share
    print("Posting...")
    find_and_click(r"C:\Users\nitin\Downloads\ml\Task\share_button.png",x=1426, y=286)
    time.sleep(3)

    print(f"✅ Post published at {datetime.now()}")

# Example Usage
if __name__ == "__main__":
    image_path = r"C:\Users\nitin\Music\changeicon.png.jpg"  # Change to actual image path
    caption = "Automated with Python 🐍 #coding #automation"
    instagram_post(image_path, caption)
