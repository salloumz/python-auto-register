import subprocess
import time
import datetime

def run():
    try:
        subprocess.call(['python3', 'autoregister.py'])
    except Exception as e:
        print(e)
        run()
    finally:
        print('Execution completed.')

while datetime.datetime.now().hour == 23 and datetime.datetime.now().minute == 58:
    run()