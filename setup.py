import cryptography
import pyotp
import getpass
import shutil
import os
from config import useTOTP

print('Welcome to LionPath Sniper Setup!')

print('PSU Email: ', end='')
username = input()

password = getpass.getpass('PSU Password: ', stream=None)

if useTOTP:
    print('TOTP 2FA Setup (disable useTOTP in config.py to skip)')
    totpsecret = getpass.getpass('TOTP Secret: ', stream=None)

# Write the username and password parameters to logininfo.py
with open("logininfo.py", "w") as file:
    # Write the variable assignments to the file
    file.write(f"username = '{username}'\n")
    file.write(f"password = '{password}'\n")
    if useTOTP:
        file.write(f"totpsecret = " + f"'{totpsecret}'\n")

# not implemented yet
# print('Which semester to enroll in (which radio button to click starting from 1): ', end='')
# radnum = input()

print("Setup Complete! Run 'python3 main.py' to start the LionPath Sniper.")