from selenium import webdriver 
import time
import pyautogui

from selenium.webdriver.chrome.service import Service

chromeoptions = webdriver.ChromeOptions()

# MacOS
chromedriver = "/opt/homebrew/bin/chromedriver"
chromeoptions.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
chromeoptions.add_argument("--user-data-dir=/Users/dylank/Library/Application Support/BraveSoftware/Brave-Browser/Default")


driver = webdriver.Chrome(service=Service(chromedriver), options=chromeoptions)

driver.get("brave://newtab")

time.wait(15)

driver.close