# TODO: add github actions workflow
# TODO: use find_elements rather than find_element with a try catch exception 
# Enable Raised Exceptions in vscode for debugging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from sys import platform
import time
import datetime
import hashlib
import pyotp
from selenium.webdriver.chrome.service import Service
from config import *
from logininfo import *

def autoregister():
    # TODO: add chrome headless support
    try:
        if platform == "linux":
            # Linux
            print('Running on Linux')
            options = webdriver.ChromeOptions()
            if useBrave:
                options.binary_location = '/usr/bin/brave'
            if darkMode:
                options.add_argument("--force-dark-mode")
                options.add_argument("--enable-features=WebContentsForceDark")
            # enable hardware acceleration on linux
            options.add_argument("--enable-features=VaapiVideoEncoder,VaapiVideoDecoder")
            options.add_argument("--enable-gpu-rasterization")
            driver = webdriver.Chrome(options=options)
        elif platform == "darwin":
            # MacOS
            print('Running on macOS')
            options = webdriver.ChromeOptions()
            if useBrave:
                options.binary_location = "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
            if darkMode:
                options.add_argument("--force-dark-mode")
                options.add_argument("--enable-features=WebContentsForceDark")    
            driver = webdriver.Chrome(options=options)
        elif platform == "win32":
            # Windows
            print('Running on Windows')
            if useEdge:
                options = webdriver.EdgeOptions()
            else:
                options = webdriver.ChromeOptions()
            if darkMode:
                if not useEdge:
                    options.add_argument("--force-dark-mode")
                options.add_argument("--enable-features=WebContentsForceDark")
            if useBrave:
                options.binary_location = "C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"
                driver = webdriver.Chrome(options=options)
            elif useEdge:
                driver = webdriver.Edge(options=options)
            else:
                driver = webdriver.Chrome(options=options)
        else:
            # may add BSD support in the future
            print(platform + ' is not supported.')

        # add another useless feature: discord rich presence
        if discordRPC:
            from pypresence import Presence
            RPC = Presence('1111876285938020493')
            # with state 'Logging in,' large image 'sniper', large text 'LionPath Sniper', and start time as current time, and a button called 'LionPath Sniper' that links to the github page
            RPC.connect()
            currentstate='Logging in...'
            RPC.update(state=currentstate, large_image='sniperrpc', large_text='LionPath Sniper', start=time.time())

        # TODO: fix chromedriver not connecting
        # we need to maximize the window so that all elements are visible
        driver.maximize_window()
        lionpath = "https://lionpath.psu.edu/"
        enrollmentPage = "https://www.lionpath.psu.edu/psc/CSPRD/EMPLOYEE/SA/c/NUI_FRAMEWORK.PT_AGSTARTPAGE_NUI.GBL?CONTEXTIDPARAMS=TEMPLATE_ID%3aPTPPNAVCOL&scname=PE_PT_NVF_ENROLLMENT&PanelCollapsible=Y&PTPPB_GROUPLET_ID=PE_PT_NVI_ENROLLMENT&CRefName=PE_PT_NVI_ENROLLMENT&AJAXTransfer=y"
        driver.get(enrollmentPage)

        # # grab username from file
        # usernameFile = open('username.txt', 'r')
        # username = usernameFile.read()
        # usernameFile.close()

        # # get password from file
        # passwordFile = open('password.txt', 'r')
        # password = passwordFile.read()
        # passwordFile.close()

        # if useTOTP:
        #     # get totp token from file
        #     totpfile = open('totpsecret.txt', 'r')
        #     totpsecret = totpfile.read()
        #     totpfile.close()

        # Login

        # Wait for login page
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'loginfmt')))

        # Type username
        driver.find_element(By.NAME, 'loginfmt').send_keys(username + '\n')
        
        # Send enter key
        # driver.find_element(By.NAME, 'loginfmt').send_keys(u'\ue007')

        # Wait for password page
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'passwd')))

        # Type password
        driver.find_element(By.NAME, 'passwd').send_keys(password)
        time.sleep(1)

        # Send enter key
        driver.find_element(By.NAME, 'passwd').send_keys(u'\ue007')

        if useTOTP:
            # Wait for totp page
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.NAME, 'otc')))

            # Create a TOTP object with the given secret
            totp = pyotp.TOTP(totpsecret, digits=6, digest=hashlib.sha1)

            # Get the current TOTP code
            totpcode = totp.now()

            # Type totp code
            driver.find_element(By.NAME, 'otc').send_keys(totpcode)
            # Send enter key
            driver.find_element(By.NAME, 'otc').send_keys(u'\ue007')

            # If the expected verification code is not entered, we need to try a different one
            # check for id 'ViewDetails' or the login page
            while True:
                # if the view details button is visible, we are on the login page
                if driver.find_elements(By.ID, 'ViewDetails'):
                    raise Exception('You didn\'t enter an expected verification code. Please try again.')
                # if the view details button is not visible, we are on the enrollment page
                elif driver.find_elements(By.ID, 'main_target_win0'):
                    break
        else:
            # wait for the enrollment page
            # TODO: send system notifications?
            print('Please type your 2FA code and continue.')
            while True:
                if driver.find_elements(By.ID, 'main_target_win0'):
                    break

        # Wait for the iframe to become visible
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'main_target_win0')))

        if discordRPC:
            currentstate='Selecting semester'
            RPC.update(state=currentstate, large_image='sniperrpc', large_text='LionPath Sniper', start=time.time())

        # Switch to the iframe
        driver.switch_to.frame(driver.find_element(By.ID, 'main_target_win0'))

        # we can automatically detect the buttons by using the id's and x
        # create a list of all the buttons and iterate through them
        radioList = []
        while True:
            if driver.find_elements(By.ID, 'SSR_DUMMY_RECV1$sels$' + str(len(radioList)) + '$$0'):
                radioList.append(driver.find_element(By.ID, 'SSR_DUMMY_RECV1$sels$' + str(len(radioList)) + '$$0'))
            else:
                break
        # pick the radio button using the enrollnum
        ActionChains(driver).click(radioList[radnum - 1]).perform()

        # Click continue
        continueButton = driver.find_element(By.ID, 'DERIVED_SSS_SCT_SSR_PB_GO')
        continueButton.click()

        # Wait for the loading screen to go away
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.ID, 'WAIT_win0')))

        # get out of the iframe
        driver.switch_to.default_content()

        # Go directly to the shopping cart url
        driver.get('https://www.lionpath.psu.edu/psc/CSPRD_newwin/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_SHOP_CART_FL.GBL?NavColl=true')

        if discordRPC:
            currentstate='In shopping cart'
            RPC.update(state=currentstate, large_image='sniperrpc', large_text='LionPath Sniper', start=time.time())

        # refresh to unglitch the page
        driver.refresh()

        if datetime.datetime.now().hour != 0 and waitUntil12AM:
            print('Waiting for 12AM')
            if discordRPC:
                currentstate='Waiting for 12AM'
                RPC.update(state=currentstate, large_image='sniperrpc', large_text='LionPath Sniper', start=time.time())
            # Wait until 12AM
            while datetime.datetime.now().hour != 0:
                # check if the "Your session is about to expire" popup is visible
                # if it is, run javascript:pingServer("https://www.lionpath.psu.edu/psc/CSPRD_2/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_SHOP_CART_FL.GBL?NavColl=true");setupTimeout2();closeLastModal();
                if driver.find_elements(By.ID, '#ICOK'):
                    driver.execute_script('pingServer("https://www.lionpath.psu.edu/psc/CSPRD_2/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_SHOP_CART_FL.GBL?NavColl=true");setupTimeout2();closeLastModal();')
                # check if the "Your session has expired" popup is visible
                # if it is, raise an exception to stop execution
                if driver.find_elements(By.XPATH, '//*[@id="login"]/div/div/div/p[4]/a'):
                    raise Exception('Your session has expired. Please log in again.')
                # increase interval if the program is using too many resources
                time.sleep(0.1)

        # refresh the page to reveal the enroll button
        driver.refresh()

        # Wait for the enroll button to appear
        while not driver.find_element(By.XPATH, '//*[@id="DERIVED_SSR_FL_SSR_ENROLL_FL"]').is_displayed():
            # refresh the page
            print('Waiting for enroll button to appear')
            driver.refresh()

        # create a list of all the checkboxes
        # checkboxes are in the format DERIVED_REGFRM1_SSR_SELECT$x where x is the number of the checkbox starting from 0
        checkboxList = []
        while True:
            if driver.find_elements(By.ID, 'DERIVED_REGFRM1_SSR_SELECT$' + str(len(checkboxList))):
                checkboxList.append(driver.find_element(By.ID, 'DERIVED_REGFRM1_SSR_SELECT$' + str(len(checkboxList))))
            else:
                break
        # click all the checkboxes in the list
        for i in range(len(checkboxList)):
            ActionChains(driver).click(checkboxList[i - 1]).perform()

        # Hit the enroll button
        # Run the javascript to click the enroll button
        driver.execute_script("javascript:submitAction_win2(document.win2,'DERIVED_SSR_FL_SSR_ENROLL_FL');")

        # Wait for yes button to appear
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="#ICYes"]')))

        # Run the javascript to click the yes button
        driver.execute_script("oParentWin.submitAction_win2(oParentWin.document.win2, '#ICYes');closeMsg(null,modId);")

        # Check if any classes failed to enroll
        # success id = win0divDERIVED_REGFRM1_DESCRLONG$x where x is a number
        # fail id = win2divDERIVED_REGFRM1_DESCRLONG$x where x is a number

        # Wait for the loading screen to go away
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.ID, 'WAIT_win2')))

        if discordRPC:
            currentstate='Viewing results'
            RPC.update(state=currentstate, large_image='sniperrpc', large_text='LionPath Sniper', start=time.time())

        if exportResults:
            with open('results.csv', 'a') as f:
                f.write("Class Name" + ',' + "Result Message" + '\n')

        # check if the fail ID is displayed
        for i in range(len(checkboxList)):
            classObj = driver.find_element(By.ID, 'DERIVED_REGFRM1_DESCRLONG$' + str(i))
            className = classObj.text
            # check to see if the class was fail or success
            # if the fail element exists
            if driver.find_elements(By.ID, 'win2divDERIVED_REGFRM1_DESCRLONG$' + str(i)):
                divHTML = driver.find_element(By.ID, 'win2divDERIVED_REGFRM1_SS_MESSAGE_LONG$' + str(i)).get_attribute("innerHTML")
                # for the fail message, we need to get rid of the top 2 lines and the last 2 lines, and convert the index 0 to a string to get the fail message by itself
                failMessage = divHTML.splitlines()[2:-2][0]
                print("\"" + className + "\" failed to enroll")
                if sendDiscordNotification:
                    import requests
                    # timestamp
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                    # send a discord notification
                    data = {
                        "username" : "LionPath Sniper",
                    }
                    data["embeds"] = [
                        {
                            "title" : ":x: **" + className + "**",
                            "description" : "**" + failMessage + "**\n\n" + str(timestamp),
                            "color" : 0xff0000
                        }
                    ]
                    requests.post(discordWebhookURL, json = data)
                if exportResults:
                    with open('results.csv', 'a') as f:
                        f.write(className + ',' + failMessage + '\n')
            # else if the success element exists
            elif driver.find_elements(By.ID, 'win0divDERIVED_REGFRM1_DESCRLONG$' + str(i)):
                divHTML = driver.find_element(By.ID, 'win0divDERIVED_REGFRM1_SS_MESSAGE_LONG$' + str(i)).get_attribute("innerHTML")
                # for the success message, we need to get rid of the top 2 lines and the last 2 lines, and convert the index 0 to a string to get the success message by itself
                successMessage = divHTML.splitlines()[2:-2][0]
                print("\"" + className + "\" enrolled successfully")
                if sendDiscordNotification:
                    import requests
                    # timestamp
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                    # send a discord notification
                    data = {
                        "username" : "LionPath Sniper",
                    }
                    data["embeds"] = [
                        {
                            "title" : ":heavy_check_mark: **" + className + "**",
                            "description" : "**" + successMessage + "**\n\n" + str(timestamp),
                            "color" : 0x00ff00
                        }
                    ]
                    requests.post(discordWebhookURL, json = data)
                if exportResults:
                    with open('results.csv', 'a') as f:
                        f.write(className + ',' + successMessage + '\n')
        input('Finished. Press enter to close the program.')
        driver.close

    except Exception as e:
        print(e)
        if sendDiscordNotification:
            try:
                import requests
                # timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
                # send a discord notification
                data = {
                    "username" : "LionPath Sniper",
                }
                data["embeds"] = [
                    {
                        "title" : ":warning: **An error occured in the main function**",
                        "description" : "**" + str(e) + "**\n\n" + str(timestamp),
                        "color" : 0xffff00
                    }
                ]
                requests.post(discordWebhookURL, json = data)
            except:
                pass
        if restartOnError:
            driver.close()
            autoregister()
        else:
            input('Press enter to close the program.')
            driver.close()
            exit()

def waitTimer():
    while True:
        time.sleep(1)
        # wait until 11:57 PM, 3 minutes before the registration window opens
        if datetime.datetime.now().hour == 23 and datetime.datetime.now().minute == 57:
            autoregister()
                

if __name__ == '__main__':
    if waitTimerEnable:
        waitTimer()
    else:
        autoregister()