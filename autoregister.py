# TODO: Create functions for each step and allow disabling of certain steps
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from sys import platform
import time
import datetime
import pyautogui
import hashlib
import pyotp

from selenium.webdriver.chrome.service import Service

chromeoptions = webdriver.ChromeOptions()

# TODO: Add support for Windows
# TODO: Add support for other browsers
# Brave Browser
if platform == "linux" or platform == "linux2":
    # Linux, chromedriver, Brave
    print('Linux')
    chromedriver = "/usr/bin/chromedriver"
    chromeoptions.binary_location = '/usr/bin/brave'
    chromeoptions.add_argument("--enable-features=VaapiVideoEncoder,VaapiVideoDecoder")
    chromeoptions.add_argument("--enable-gpu-rasterization")
    # chromeoptions.add_argument("--user-data-dir=brave-data-dir")
    # chromeoptions.add_argument("--user-data-dir=/home/dylank/.config/BraveSoftware/Brave-Browser")
elif platform == "darwin":
    # MacOS, chromedriver, Brave
    print('macOS')
    chromedriver = "/opt/homebrew/bin/chromedriver"
    chromeoptions.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    # chromeoptions.add_argument("--user-data-dir=brave-data-dir")
    # chromeoptions.add_argument("--user-data-dir=/Users/dylank/Library/Application Support/BraveSoftware/Brave-Browser")
else:
    print('Unsupported operating system')
driver = webdriver.Chrome(service=Service(chromedriver), options=chromeoptions)


lionpath = "https://lionpath.psu.edu/"
enrollmentPage = "https://www.lionpath.psu.edu/psc/CSPRD/EMPLOYEE/SA/c/NUI_FRAMEWORK.PT_AGSTARTPAGE_NUI.GBL?CONTEXTIDPARAMS=TEMPLATE_ID%3aPTPPNAVCOL&scname=PE_PT_NVF_ENROLLMENT&PanelCollapsible=Y&PTPPB_GROUPLET_ID=PE_PT_NVI_ENROLLMENT&CRefName=PE_PT_NVI_ENROLLMENT&AJAXTransfer=y"
driver.get(enrollmentPage)

# grab username from file
usernameFile = open('username.txt', 'r')
username = usernameFile.read()
usernameFile.close()

# TODO: Fix the next button not being clicked
# TODO: We can do this by using a try catch and hitting enter again if it fails
# get password from file
passwordFile = open('password.txt', 'r')
password = passwordFile.read()
passwordFile.close()

# TODO: Fix "You didn't enter an expected verification code. Please try again."
# get totp token from file
totpfile = open('totpsecret.txt', 'r')
totpsecret = totpfile.read()
totpfile.close()

# Login

# Wait for login page
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'loginfmt')))

# Type username
driver.find_element(By.NAME, 'loginfmt').send_keys(username)

# Wait for password page
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'passwd')))

# Type password
driver.find_element(By.NAME, 'passwd').send_keys(password)
time.sleep(1)

# Send enter key
driver.find_element(By.NAME, 'passwd').send_keys(u'\ue007')

# Wait for totp page
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'otc')))

# Create a TOTP object with the given secret
totp = pyotp.TOTP(totpsecret, digits=6, digest=hashlib.sha1)

# Get the current TOTP code
totpcode = totp.now()

# Type totp code
driver.find_element(By.NAME, 'otc').send_keys(totpcode)
# Send enter key
driver.find_element(By.NAME, 'otc').send_keys(u'\ue007')

# Wait for the iframe to become visible
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'main_target_win0')))

# Switch to the iframe
driver.switch_to.frame(driver.find_element(By.ID, 'main_target_win0'))

# Radio buttons for each semester
radio1 = driver.find_element(By.ID, 'SSR_DUMMY_RECV1$sels$0$$0')
radio2 = driver.find_element(By.ID, 'SSR_DUMMY_RECV1$sels$1$$0')
radio3 = driver.find_element(By.ID, 'SSR_DUMMY_RECV1$sels$2$$0')

radiobtn = radio3

# Select the radio button by clicking on it with actionchains
ActionChains(driver).click(radiobtn).perform()


# Click continue
continueButton = driver.find_element(By.ID, 'DERIVED_SSS_SCT_SSR_PB_GO')
continueButton.click()

# Wait for the loading screen to go away
WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))

# get out of the iframe
driver.switch_to.default_content()

# Go to the shopping cart
# Method 1: Click the shopping cart button
# shoppingCartButton = driver.find_element(By.XPATH, '//*[@id="win1divPTGP_STEP_DVW_PTGP_STEP_BTN_GB$4"]')
# ActionChains(driver).click(shoppingCartButton).perform()
# Method 2: Go directly to the shopping cart url
driver.get('https://www.lionpath.psu.edu/psc/CSPRD_newwin/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_SHOP_CART_FL.GBL?NavColl=true')

# wait for the loading screen to go away
# (only needed if we use method 1)
# WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))

# how many classes are you enrolling in?
# TODO: we can auto detect this by counting the number of checkboxes
enrollnum = 2

# Method 1: click the enroll button to unglitch the page
# enrollButton = driver.find_element(By.ID, 'DERIVED_SSR_FL_SSR_ENROLL_FL')
# ActionChains(driver).click(enrollButton).perform()
# WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))
# time.sleep(0.1)

# Method 2: refresh to unglitch the page
# refresh the page
driver.refresh()

# Wait until 12AM
# while it's not 12AM
while datetime.datetime.now().hour != 0:
    # wait 1 second
    time.sleep(0.5)
    # refresh the page
    print('Waiting for 12AM')

# refresh the page to reveal the enroll button
driver.refresh()

# TODO: attempt to check if the enroll button is visible, otherwise refresh the page
while not driver.find_element(By.ID, 'DERIVED_SSR_FL_SSR_ENROLL_FL').is_displayed():
    # refresh the page
    print('Waiting for enroll button to appear')
    driver.refresh()


# checkboxes are in the format DERIVED_REGFRM1_SSR_SELECT$x where x is the number of the checkbox starting from 0 and going to enrollnum - 1
for i in range(enrollnum):
    checkbox = driver.find_element(By.ID, 'DERIVED_REGFRM1_SSR_SELECT$' + str(i))
    ActionChains(driver).click(checkbox).perform()

# Hit the enroll button
enrollButton = driver.find_element(By.ID, 'DERIVED_SSR_FL_SSR_ENROLL_FL')
ActionChains(driver).click(enrollButton).perform()

# Wait for yes button to appear
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, '#ICYes')))

# Run the javascript to click the yes button
driver.execute_script("oParentWin.submitAction_win2(oParentWin.document.win2, '#ICYes');closeMsg(null,modId);")

input('Finished. Press enter to close the program.')

driver.close
