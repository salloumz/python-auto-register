from selenium import webdriver
from selenium.webdriver.common.by import By
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
lionpath = "https://lionpath.psu.edu/"
driver.get(lionpath)


input('Press enter to continue after logging in')
time.sleep(1)

enrollment_button = driver.find_element(By.LINK_TEXT, "Enrollment")
# enrollment_btn = enrollment_button.find_element(By.CLASS_NAME, "ps-link")
print(enrollment_button)
enrollment_button.click

time.sleep(1)

driver.close