import subprocess
import time
import datetime

while datetime.datetime.now().hour == 23 and datetime.datetime.now().minute == 58:
    subprocess.call(['python3', 'autoregister.py'])