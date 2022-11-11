import time
from selenium import webdriver

from selenium.webdriver.chrome.service import Service

chromedriver = "/usr/bin/chromedriver"

option = webdriver.ChromeOptions()

option.binary_location = '/usr/lib/brave-bin/brave'

option.add_argument("--user-data-dir=/home/dylank/.config/BraveSoftware/Brave-Browser")
option.add_argument("--enable-features=VaapiVideoEncoder,VaapiVideoDecoder")
option.add_argument("--enable-gpu-rasterization")

s = Service(chromedriver)

driver = webdriver.Chrome(service=s, options=option)

driver.get("chrome://newtab")

x = 1

while x == 1:
    val = input("Enter your value: ")
    print(val)
    print(x)
    x = val

driver.close()
