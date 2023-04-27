# TODO: Create functions for each step and allow disabling of certain steps
# TODO: Clean up code comments
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from sys import platform
import time
import pyautogui
import hashlib
import pyotp

from selenium.webdriver.chrome.service import Service

chromeoptions = webdriver.ChromeOptions()

# TODO: Add support for Windows
# TODO: Add support for other browsers
if platform == "linux" or platform == "linux2":
    # Linux
    print('Linux')
    chromedriver = "/usr/bin/chromedriver"
    chromeoptions.binary_location = '/usr/bin/brave'
    chromeoptions.add_argument("--enable-features=VaapiVideoEncoder,VaapiVideoDecoder")
    chromeoptions.add_argument("--enable-gpu-rasterization")
    # chromeoptions.add_argument("--user-data-dir=/home/dylank/.config/BraveSoftware/Brave-Browser")
elif platform == "darwin":
    # MacOS
    print('macOS')
    chromedriver = "/opt/homebrew/bin/chromedriver"
    chromeoptions.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
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
# get password from file lmao
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

# Wait
# time.sleep(1)

# Wait for password page
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'passwd')))

# Type password
driver.find_element(By.NAME, 'passwd').send_keys(password)
time.sleep(1)

# Send enter key
driver.find_element(By.NAME, 'passwd').send_keys(u'\ue007')


WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'otc')))

# Generate totp code
# Create a TOTP object with the given secret
totp = pyotp.TOTP(totpsecret, digits=6, digest=hashlib.sha1)

# Get the current TOTP code
totpcode = totp.now()

# Type totp code
driver.find_element(By.NAME, 'otc').send_keys(totpcode)
# Send enter key
driver.find_element(By.NAME, 'otc').send_keys(u'\ue007')


# Wait until push accepted lionpath is loaded, we are waiting for the enrollment button
# WebDriverWait(driver, 240).until(EC.presence_of_element_located((By.ID, 'PE_UI020_BTNS_PE_GRID_BUTTON$1')))


# input('Press enter to continue after logging in')

# driver.find_element(By.ID, "win0divPE_UI020_BTNS_PE_GRID_BUTTON$1")
# enrollment_button = driver.find_element(By.ID, "PE_UI020_BTNS_PE_GRID_BUTTON$span$1")
# enrollment_button = driver.find_element(By.NAME, "Enrollment")
# print(enrollment_button)
# enrollment_button.click
# enrollment_button.click

# hit the enrollment button

# driver.execute_script("submitAction_win0(document.win0,'PE_UI020_BTNS_PE_GRID_BUTTON$1')")

# go to the enrollment page

# driver.get('https://www.lionpath.psu.edu/psc/CSPRD/EMPLOYEE/SA/c/NUI_FRAMEWORK.PT_AGSTARTPAGE_NUI.GBL?CONTEXTIDPARAMS=TEMPLATE_ID%3aPTPPNAVCOL&scname=PE_PT_NVF_ENROLLMENT&PanelCollapsible=Y&PTPPB_GROUPLET_ID=PE_PT_NVI_ENROLLMENT&CRefName=PE_PT_NVI_ENROLLMENT&AJAXTransfer=y')

# Wait until the page is loaded
# WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'DERIVED_SSS_SCT_SSR_PB_GO')))

# Go directly to the iframe page
# driver.get('https://www.lionpath.psu.edu/psc/CSPRD/EMPLOYEE/SA/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?NavColl=true&ICAGTarget=start&ICAJAXTrf=true')

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
enrollnum = 2

# click the enroll button to unglitch the page
enrollButton = driver.find_element(By.ID, 'DERIVED_SSR_FL_SSR_ENROLL_FL')
ActionChains(driver).click(enrollButton).perform()
# TODO: Wait for the loading screen to go away
time.sleep(0.5)

# checkboxes are in the format DERIVED_REGFRM1_SSR_SELECT$x where x is the number of the checkbox starting from 0 and going to enrollnum - 1
for i in range(enrollnum):
    checkbox = driver.find_element(By.ID, 'DERIVED_REGFRM1_SSR_SELECT$' + str(i))
    ActionChains(driver).click(checkbox).perform()

# Hit the enroll button
enrollButton = driver.find_element(By.ID, 'DERIVED_SSR_FL_SSR_ENROLL_FL')
ActionChains(driver).click(enrollButton).perform()

# # if lionpath glitches, it will load the iframe from earlier, print out if this happens
# while not driver.find_elements(By.ID, '#ICYes'):
#     if driver.find_elements(By.ID, 'main_target_win0'):
#         print('iframe detected, we need to go back to the shopping cart')
#         shoppingCartButton = driver.find_element(By.XPATH, '//*[@id="win2divPTGP_STEP_DVW_PTGP_STEP_BTN_GB$4"]')
#         ActionChains(driver).click(shoppingCartButton).perform()
#         # wait for the loading screen to go away
#         WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))
#         for i in range(enrollnum):
#             checkbox = driver.find_element(By.ID, 'DERIVED_REGFRM1_SSR_SELECT$' + str(i))
#             ActionChains(driver).click(checkbox).perform()
#         # Hit the enroll button
#         enrollButton = driver.find_element(By.ID, 'DERIVED_REGFRM1_LINK_ADD_ENRL$291$')
#         ActionChains(driver).click(enrollButton).perform()

# Wait for yes button to appear
WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, '#ICYes')))

# time.sleep(0.5)

# "Are you sure you want to enroll?"
# Confirmation Method 1: Click the yes button
# yesButton = driver.find_element(By.ID, '#ICYes')
# noButton = driver.find_element(By.ID, '#ICNo')
# buttonToClick = yesButton
# ActionChains(driver).click(buttonToClick).perform()
# Confirmation Method 2: Tab to the yes button and hit enter
# yesButton = driver.find_element(By.ID, '#ICYes')
# noButton = driver.find_element(By.ID, '#ICNo')
# buttonToClick = yesButton
# ActionChains(driver).send_keys_to_element(buttonToClick, u'\ue004').perform()
# ActionChains(driver).send_keys_to_element(buttonToClick, u'\ue007').perform()
# Confirmation Method 3: Run the javascript to click the yes button
driver.execute_script("oParentWin.submitAction_win2(oParentWin.document.win2, '#ICYes');closeMsg(null,modId);")

# time.sleep(3)

# # You can select the semester based on the row that it's on
# # Semesters
# row1 = driver.find_element(By.XPATH, '//*[@id="GRID_TERM_SRC5$0_row_0"]/td')
# row2 = driver.find_element(By.XPATH, '//*[@id="GRID_TERM_SRC5$0_row_1"]/td')
# row3 = driver.find_element(By.XPATH, '//*[@id="GRID_TERM_SRC5$0_row_2"]/td')

# # Click current semester
# semester = row2
# ActionChains(driver).click(semester).perform()

# time.sleep(1)

# # Trying to hit shopping cart button
# # driver.execute_script("cancelBubble(event);if (!top.ptgpPage.openCustomStepButton('PE_S201901181129161770441332')) top.ptgpPage.openUrlWithWarning(this.getAttribute('href'), 'top.ptgpPage.selectStep(\'PE_S201901181129161770441332\');', true);return false;)")
# # driver.sleep fix this pls
# # shoppingCartButton = driver.find_element(By.XPATH, '//*[@id="win2divPTGP_STEP_DVW_PTGP_STEP_BTN_GB$4"]')
# ActionChains(driver).click(shoppingCartButton).perform()

input('Enroll?')
time.sleep(1)

# Hit the enroll button

time.sleep(1)

driver.close
