# Config Options
# Which semester are you enrolling in? (Which radio button should be selected?)
radnum = 2
# How many classes are you enrolling in?
# TODO: we can auto detect this by counting the number of checkboxes
enrollnum = 2
# Should we wait until 12AM to enroll?
waitUntil12AM = False
# Is TOTP enabled for this Microsoft account? If so, it can be automated in the script
useTOTP = True
# [Windows, Mac, Linux] Brave Support (instead of Chrome or Edge)
useBrave = False
# [Windows] Microsoft Edge Support (instead of Chrome)
useEdge = True
# Should we send a notification in Discord with results/if a class fails to enroll?
sendDiscordNotification = False
# Discord Webhook URL
discordWebhookURL = ""
# Experimental // Development
# Create a file with the results?
resultFile = "None"
# Should we send an email with results/if a class fails to enroll?
sendEmailNotification = False
