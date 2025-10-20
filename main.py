# TODO: pytest support
# Enable Raised Exceptions in vscode for debugging
# TODO: conditional imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from sys import platform
import time
import datetime
import hashlib
import pyotp
import base64
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from config import *
# TODO: check for logininfo file
from logininfo import *

# TODO: handle discord and ntfy exceptions (for ex if an internet outage has occurred)
# TODO: handle SMTP authentication failure

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
            print(platform + ' is not supported.')

        # TODO: fix chromedriver not connecting
        # we need to maximize the window so that all elements are visible
        driver.maximize_window()
        lionpath = "https://lionpath.psu.edu/"
        enrollmentPage = "https://www.lionpath.psu.edu/psc/CSPRD_7/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_SHOP_CART_FL.GBL?NavColl=true"
        driver.get(enrollmentPage)

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

        # fix "please enter your password"
        if driver.find_elements(By.ID, 'passwordError'):
            # enter password again
            driver.find_element(By.NAME, 'passwd').send_keys(password)
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
                elif driver.find_elements(By.ID, 'win7divPSPAGECONTAINER'):
                    break
        else:
            # wait for the enrollment page
            # TODO: send system notifications?
            print('Please type your 2FA code and continue.')
            while True:
                if driver.find_elements(By.ID, 'win7divPSPAGECONTAINER'):
                    break

        # Wait for the iframe to become visible
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'win7divPSPAGECONTAINER')))

        buttontoclick = 'win7divDERIVED_SSR_FL_SSR_GRPBOX_TERM$' + str(radnum - 1)

        semesterButton = driver.find_element(By.ID, buttontoclick)

        semesterButton.click()

        # Go directly to the shopping cart url
        # driver.get('https://www.lionpath.psu.edu/psc/CSPRD_newwin/EMPLOYEE/SA/c/SSR_STUDENT_FL.SSR_SHOP_CART_FL.GBL?NavColl=true')

        # refresh to unglitch the page
        driver.refresh()

        # create checkbox list for result determination (remove if using old method)
        checkboxList = []
        while True:
            if driver.find_elements(By.ID, 'DERIVED_REGFRM1_SSR_SELECT$' + str(len(checkboxList))):
                checkboxList.append(driver.find_element(By.ID, 'DERIVED_REGFRM1_SSR_SELECT$' + str(len(checkboxList))))
            else:
                break

        if datetime.datetime.now().hour != 0 and waitUntil12AM:
            print('Waiting for 12AM')
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
        # while not driver.find_element(By.XPATH, '//*[@id="DERIVED_SSR_FL_SSR_ENROLL_FL"]').is_displayed():
        #     # refresh the page
        #     print('Waiting for enroll button to appear')
        #     driver.refresh()
        # HACK: wait for the enroll button to appear
        # TODO: test .is_displayed() rather than try except
        while True:
            try:
                if driver.find_element(By.XPATH, '//*[@id="win0divDERIVED_SSR_FL_SSR_ENROLL_FL"]'):
                    break
            except:
                driver.refresh()

        # create a list of all the checkboxes
        # checkboxes are in the format DERIVED_REGFRM1_SSR_SELECT$x where x is the number of the checkbox starting from 0
        # checkboxList = []
        # while True:
            # if driver.find_elements(By.ID, 'DERIVED_REGFRM1_SSR_SELECT$' + str(len(checkboxList))):
                # checkboxList.append(driver.find_element(By.ID, 'DERIVED_REGFRM1_SSR_SELECT$' + str(len(checkboxList))))
            # else:
                # break
        # click all the checkboxes in the list
        # for i in range(len(checkboxList)):
            # ActionChains(driver).click(checkboxList[i - 1]).perform()

        # experimental javascript function
        clickall = """
        (function() {
            // converted code to JS
            let checkboxList = [];
            let i = 0;

            // checkboxes are in the format DERIVED_REGFRM1_SSR_SELECT$x where x is the number of the checkbox starting from 0
            while (true) {
                let checkbox = document.getElementById('DERIVED_REGFRM1_SSR_SELECT$' + i);
                if (checkbox) {
                    checkboxList.push(checkbox);
                    i++;
                } else {
                    break;
                }
            }

            // click all the checkboxes in the list
            checkboxList.forEach((checkbox) => {
                checkbox.click();
            });
        })();
        """
        driver.execute_script(clickall)

        # Hit the enroll button
        # Run the javascript to click the enroll button
        driver.execute_script("javascript:submitAction_win0(document.win0,'DERIVED_SSR_FL_SSR_ENROLL_FL');")

        # Wait for yes button to appear
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="#ICYes"]')))

        # Run the javascript to click the yes button
        driver.execute_script("oParentWin.submitAction_win2(oParentWin.document.win2, '#ICYes');closeMsg(null,modId);")

        # Check if any classes failed to enroll
        # success gif = /cs/CSPRD/cache/PS_CS_STATUS_SUCCESS_ICN_1.gif
        # fail gif = /cs/CSPRD/cache/PS_CS_STATUS_ERROR_ICN_1.gif

        # Wait for the loading screen to go away
        WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.ID, 'WAIT_win2')))

        # timestamp
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

        if sendEmailNotification:
            emailMessage = f"""
            Hello,

            Here are the results of your attempted enrollment as of {timestamp}


            """

        if exportResults:
            with open('results.csv', 'a') as f:
                f.write("Class Name" + ',' + "Result Message" + ',' + timestamp + '\n')


        # check if the fail ID is displayed
        for i in range(len(checkboxList)):
            # get the class name
            className = (driver.find_element(By.ID, 'DERIVED_REGFRM1_DESCRLONG$' + str(i))).text
            # for the message, we need to get rid of the top 2 lines and the last 2 lines, and convert the index 0 to a string to get the fail message by itself
            message = (driver.find_element(By.ID, 'win2divDERIVED_REGFRM1_SS_MESSAGE_LONG$' + str(i)).get_attribute("innerHTML")).splitlines()[2:-2][0]
            # check to see if the class was fail or success
            if message == "This class has been added to your schedule." or message == "The pre-requisite has been met conditionally. The enrollment is allowed with the condition of satisfying the pre-requisite before the start of the class." or message == "You have already taken this class. When graded this course may be subject to repeat rules. Verify that the class will apply toward your course of study.":
                print("\"" + className + "\" enrolled successfully")
                if sendDiscordNotification:
                    import requests
                    # send a discord notification
                    data = {
                        "username" : "LionPath WebSniper",
                    }
                    data["embeds"] = [
                        {
                            "title" : ":white_check_mark: **" + className + "**",
                            "description" : "**" + message + "**\n\n" + str(timestamp),
                            "color" : 0x00ff00
                        }
                    ]
                    requests.post(discordWebhookURL, json = data)
                if sendntfyNotification:
                    if ntfyRequiresAuth:
                        authHeader = "Basic " + base64.b64encode((ntfyUser + ":" + ntfyPswd).encode()).decode()
                        requests.post(ntfyURL,
                        data=message,
                        headers={
                            "Title": className,
                            "Tags": "heavy_check_mark",
                            "Authorization": authHeader
                        })
                    else:
                        requests.post(ntfyURL,
                        data=message,
                        headers={
                            "Title": className,
                            "Tags": "heavy_check_mark"
                        })
                if sendEmailNotification:
                    emailMessage += f"""
                    ✅ {className} - {message}
                    """
                if exportResults:
                    with open('results.csv', 'a') as f:
                        f.write(className + ',' + message + '\n')
            # else if error
            else:
                print("\"" + className + "\" failed to enroll")
                if sendDiscordNotification:
                    import requests
                    # send a discord notification
                    data = {
                        "username" : "LionPath WebSniper",
                    }
                    data["embeds"] = [
                        {
                            "title" : ":x: **" + className + "**",
                            "description" : "**" + message + "**\n\n" + str(timestamp),
                            "color" : 0xff0000
                        }
                    ]
                    requests.post(discordWebhookURL, json = data)
                if sendntfyNotification:
                    if ntfyRequiresAuth:
                        authHeader = "Basic " + base64.b64encode((ntfyUser + ":" + ntfyPswd).encode()).decode()
                        requests.post(ntfyURL,
                        data=message,
                        headers={
                            "Title": className,
                            "Tags": "x",
                            "Authorization": authHeader
                        })
                    else:
                        requests.post(ntfyURL,
                        data=message,
                        headers={
                            "Title": className,
                            "Tags": "x"
                        })
                if sendEmailNotification:
                    emailMessage += f"""
                    ❌ {className} - {message}
                    """
                if exportResults:
                    with open('results.csv', 'a') as f:
                        f.write(className + ',' + message + '\n')
        if sendEmailNotification:
            try:
                msg = MIMEMultipart()
                msg['Subject'] = "LionPath WebSniper Enrollment Results"
                msg['From'] = username
                msg['To'] = emailAddress
                msg.attach(MIMEText(emailMessage, 'plain'))
                server = smtplib.SMTP(smtpServer,smtpPort)
                if smtpTLS:
                    server.starttls()
                server.login(smtpUsername,smtpPassword)
                server.sendmail(smtpUsername,emailAddress,msg.as_string())
                server.quit()
            except Exception as e:
                print("Failed to send the email:" + str(e))
                import traceback
                traceback.print_exc()
                pass


        input('Finished. Press enter to close the program.')
        driver.close

    except Exception as e:
        print(e)
        import traceback
        traceback.print_exc()
        if restartOnError:
            driver.close()
            autoregister()
        else:
            input('Press enter to close the program.')
            driver.close()
            exit()

def waitTimer():
    print('Idle until 11:57 PM')
    # FIXME: display must be on to run the program
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
