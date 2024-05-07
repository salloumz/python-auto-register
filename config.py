# Config Options
# Which semester to enroll in (which radio button to click starting from 1)
radnum = 2
# Wait for 12AM to enroll
waitUntil12AM = True
# Wait until 3 minutes before 12AM to start the script
# TODO: Make time configurable
waitTimerEnable = False
# Restart the script if an error occurs
restartOnError = True
# Dark Mode
darkMode = True
# TOTP Support (2FA)
useTOTP = True
# [Windows, Mac, Linux] Brave Support (instead of Chrome or Edge)
useBrave = False
# [Windows] Microsoft Edge Support (instead of Chrome)
useEdge = True
# Discord Webhook Integration
sendDiscordNotification = False
discordWebhookURL = ""
# File to save results to, leave as "None" to disable
exportResults = True
# Ntfy Notification
sendntfyNotification = False
ntfyURL = "https://ntfy.example.com/python-auto-register"
ntfyRequiresAuth = False
ntfyUser = ""
ntfyPswd = ""
# Email Notification with results
sendEmailNotification = False
emailAddress = ""
# SMTP Settings for email notification
smtpServer = ""
smtpPort = 0
smtpTLS = True
smtpUsername = ""
smtpPassword = ""