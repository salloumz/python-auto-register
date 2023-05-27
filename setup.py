import cryptography
import pyotp
import getpass
import shutil
import os
from cryptography.fernet import Fernet
from config import useTOTP

# check if login folder exists
# if not, prompt the user to run the setup
if not os.path.exists('login'):
    # create login folder
    os.mkdir('login')
else:
    # check if the login folder is empty
    if os.listdir('login'):
        # if not empty, prompt the user to run the setup
        print('Login folder exists and is not empty. Would you like to re-run the setup? (y/n): ', end='')
        rerun = input()
        if rerun == 'y':
            shutil.rmtree('login')
            os.mkdir('login')
        else:
            exit()

print('Welcome to LionPath Sniper Setup!')

print('PSU Email: ', end='')
username = input()

# write the username to login/username.txt
with open('login/username.txt', 'w') as fileusername:
    fileusername.write(username)

password = getpass.getpass('PSU Password: ', stream=None)

# write the password to login/password.txt
with open('login/password.txt', 'w') as filepassword:
    filepassword.write(password)

if useTOTP:
    print('TOTP 2FA Setup (disable useTOTP in config.py to skip)')
    print('TOTP Secret: ', end='')
    totpsecret = input()

    # write the totp secret to login/totpsecret.txt
    with open('login/totpsecret.txt', 'w') as filetotpsecret:
        filetotpsecret.write(totpsecret)

    print("Setup Complete! Run 'python3 main.py' to start the LionPath Sniper.")