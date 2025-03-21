import smtplib
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"  # Using Gmail's SMTP server
SMTP_PORT = 587
EMAIL_SENDER = "kmsumanth002@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "fgwm oktv jvvd qiym"  # Replace with your email app password
EMAIL_RECEIVER = "kmsumanth08@gmail.com"  # Replace with recipient email

# ✅ Email Body
subject = "🚀 Test Email: Fraud Alert System"
body = "This is a test email to verify if SMTP works."

msg = MIMEText(body, "plain")
msg["Subject"] = subject
msg["From"] = EMAIL_SENDER
msg["To"] = EMAIL_RECEIVER

try :
    server = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)
    server.starttls()
    server.login(EMAIL_SENDER,EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER,EMAIL_RECEIVER,msg.as_string())
    server.quit()
    print("testing mail sent succefully")
except Exception as e :
    print(e)