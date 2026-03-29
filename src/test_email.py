import smtplib
from email.mime.text import MIMEText

sender_email = "testmailanish007@gmail.com"
app_password = "gcrx vxik bnwk aawl"
receiver_email = "anishmadhavs@gmail.com"

subject = "Test Email from AI Project"
message = "This is a test email from Predictive Maintenance System."

msg = MIMEText(message)
msg['Subject'] = subject
msg['From'] = sender_email
msg['To'] = receiver_email

try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, app_password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.quit()
    print("Test Email Sent Successfully!")
except Exception as e:
    print("Error:", e)