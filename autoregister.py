from selenium import webdriver 
from sys import platform
import time
import pyautogui

from selenium.webdriver.chrome.service import Service

chromeoptions = webdriver.ChromeOptions()

if platform == "linux" or platform == "linux2":
    # linux
    print('linux')
elif platform == "darwin":
    # OS X
    print('macOS')
elif platform == "win32":
    # Windows...
    print('windows')

# MacOS
chromedriver = "/opt/homebrew/bin/chromedriver"
chromeoptions.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
chromeoptions.add_argument("--user-data-dir=/Users/dylank/Library/Application Support/BraveSoftware/Brave-Browser")


driver = webdriver.Chrome(service=Service(chromedriver), options=chromeoptions)

driver.get("brave://newtab")

time.wait(15)



driver.close