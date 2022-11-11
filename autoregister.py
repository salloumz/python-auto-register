from selenium import webdriver 
from sys import platform
import time
import pyautogui

from selenium.webdriver.chrome.service import Service

chromeoptions = webdriver.ChromeOptions()

if platform == "linux" or platform == "linux2":
    # Linux
    print('Linux')
    chromedriver = "/usr/bin/chromedriver"
    chromeoptions.binary_location = '/usr/lib/brave-bin/brave'
    chromeoptions.add_argument("--user-data-dir=/home/dylank/.config/BraveSoftware/Brave-Browser")
    chromeoptions.add_argument("--enable-features=VaapiVideoEncoder,VaapiVideoDecoder")
    chromeoptions.add_argument("--enable-gpu-rasterization")
elif platform == "darwin":
    # MacOS
    print('macOS')
    chromedriver = "/opt/homebrew/bin/chromedriver"
    chromeoptions.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    chromeoptions.add_argument("--user-data-dir=/Users/dylank/Library/Application Support/BraveSoftware/Brave-Browser")
else:
    print('Unsupported operating system')


driver = webdriver.Chrome(service=Service(chromedriver), options=chromeoptions)

driver.get("https://lionpath.psu.edu/")

input('Press enter to continue after logging in')
time.sleep(1)

enrollment_button = chromedriver.find_element_by_link_text("Enrollment")
enrollment_button.click

driver.close