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
# Experimental // Not fully implemented
# Should we send a notification in Discord with results/if a class fails to enroll?
sendDiscordNotification = False
# Discord Webhook URL
discordWebhookURL = ""
# Should we send an email with results/if a class fails to enroll?
sendEmailNotification = False
# Should we use the Brave Browser instead of the built in one?
useBrave = False