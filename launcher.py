import subprocess
import time
import datetime

def discordNotification(message):
    from config import sendDiscordNotification, discordWebhookURL
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
                "title" : ":warning: **An exception occurred**",
                "description" : "**" + message + "**\n\n" + str(timestamp),
                "color" : 0xff0000
            }
        ]
        requests.post(discordWebhookURL, json = data)
    
def run():
    try:
        subprocess.check_call(['python3', 'autoregister.py'])
    except subprocess.CalledProcessError as e:
        discordNotification(str(e))
        print(e)
        run()
    finally:
        print('Execution completed.')

def waitToRun():
    while True:
        time.sleep(1)
        if datetime.datetime.now().hour == 23 and datetime.datetime.now().minute == 57:
            run()

# run()
waitToRun()