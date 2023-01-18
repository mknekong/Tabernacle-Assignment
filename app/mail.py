#To help keep your account secure, from May 30, 2022,
# Google no longer supports the use of third-party apps or devices
# which ask you to sign in to your Google Account using only your username and password.

import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def Mail(toaddr, subject, body):
    fromaddr = "ro.khmhq@gmail.com"
    pw = "88888"

    message = MIMEMultipart()
    message["From"] = fromaddr
    message["To"] = toaddr
    message["Subject"] = subject
    message["Bcc"] = toaddr

    #Mail Body
    message.attach(MIMEText(body,"plain"))
    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com",456,context=context) as server:
        server.login(fromaddr,pw)
        server.sendmail(fromaddr,toaddr,text)