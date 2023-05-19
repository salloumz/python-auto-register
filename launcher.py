import subprocess
import time
import datetime
from config import *

def run():
    try:
        subprocess.check_call(['python3', 'autoregister.py'])
    except subprocess.CalledProcessError as e:
        # TODO: discord notification
        print(e)
        run()
    finally:
        print('Execution completed.')

while datetime.datetime.now().hour == 23 and datetime.datetime.now().minute == 58:
    run()

# run()