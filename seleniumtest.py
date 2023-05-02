import time
from selenium import webdriver

from selenium.webdriver.chrome.service import Service

# Set the path to the chromedriver executable
chromedriver = "/usr/bin/chromedriver"

# Set the path to the Brave executable
brave_location = "/usr/lib/brave-bin/brave"

# Set the path to the Brave profile
brave_profile = "/home/dylank/.config/BraveSoftware/Brave-Browser"

# Create a ChromeOptions object
option = webdriver.ChromeOptions()

# Set the binary location
option.binary_location = brave_location

# Set the user data directory
option.add_argument(f"--user-data-dir={brave_profile}")

# Enable hardware acceleration
option.add_argument("--enable-features=VaapiVideoEncoder,VaapiVideoDecoder")

# Enable GPU rasterization
option.add_argument("--enable-gpu-rasterization")

# Create a Service object
s = Service(chromedriver)

# Create a ChromeDriver object
driver = webdriver.Chrome(service=s, options=option)

# Open a new tab
driver.get("chrome://newtab")

# Create a variable to hold the loop state
running = True

# Run the loop until the user enters 'stop'
while running:
    # Ask the user for input
    val = input("Enter your value: ")

    # Print the user's input
    print(val)

    # If the user entered 'stop', stop the loop
    if val == "stop":
        running = False

# Close the browser
driver.close()
