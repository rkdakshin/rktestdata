import pyautogui
import time
"""
print("Hello world")

#mouse operation
pyautogui.click(100,100)
time.sleep(4)
pyautogui.rightClick(100,100)
time.sleep(4)
pyautogui.scroll(-500)
time.sleep(3)
pyautogui.click(1336,674)
time.sleep(2)
pyautogui.rightClick(1336,674)
time.sleep(2)
pyautogui.scroll(500)
time.sleep(2)
pyautogui.click(1108,968)
time.sleep(6)
pyautogui.typewrite('python findmouseposition.py')
time.sleep(1)
pyautogui.press('Enter')
time.sleep(2)
pyautogui.click(1028,316)
time.sleep(1)
pyautogui.hotkey('ctrl','a')
time.sleep(2)
"""
location = pyautogui.locateOnScreen('image.png',confidence=0.8)
print(location)
pyautogui.click(pyautogui.center(location))
ss = pyautogui.screenshot()
ss.save("demo.png")
