# -*- coding:utf-8 -*-
# @module emailip
# @desc Send ip to email
# @since 2022.02.24, 04:55
# @changed 2022.02.24, 04:58
# See:
# https://www.instructables.com/Raspberry-Pi-Motion-Detection-Security-Camera/

# NOTE: Start local smtp server with: `sudo python -m smtpd -c DebuggingServer -n localhost:1025`
# Or use ssmpt:
# ```
# sudo apt-get install ssmtp
# ```

import socket
import smtplib
import os

from email.message import EmailMessage
#  from email.mime.text import MIMEText
#  from email.MIMEMultipart import MIMEMultipart
#  from email.MIMEText import MIMEText


def getIPAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print(s.getsockname()[0])
    ipAddr = s.getsockname()[0]
    s.close()
    return ipAddr


def sendIpMsg(hostName=None, ipAddr=None):

    fromAddr = '"rpi-service" <dmia@yandex.ru>'
    toAddr = 'lilliputten@yandex.ru'

    subject = f"Raspberry started on {ipAddr} ({hostName})"
    content = f"Raspberry started on:\n\nHost: {hostName}\nIP: {ipAddr}\n"

    msg = EmailMessage()
    msg.set_content(content)

    msg['Subject'] = subject
    msg['From'] = fromAddr
    msg['To'] = toAddr

    port = 1025
    s = smtplib.SMTP('localhost', port)
    s.send_message(msg)
    s.quit()


hostName = os.getenv('HOST')  # Unix
if not hostName:
    hostName = os.getenv('COMPUTERNAME')  # Windows

ipAddr = getIPAddress()

print('ipAddr:', ipAddr)
print('hostName:', hostName)

print('Start sending:', hostName, ipAddr)

sendIpMsg(hostName=hostName, ipAddr=ipAddr)

#  fromaddr = "YOUR ADDRESS"
#  toaddr = "RECEIVING ADDRESS"
#  msg = MIMEMultipart()
#  msg['From'] = fromaddr
#  msg['To'] = toaddr
#  msg['Subject'] = "IP Address"
#  body = msg.attach(MIMEText(body, 'plain'))
#  server = smtplib.SMTP('smtp.gmail.com', 587)
#  server.starttls()
#  server.login(fromaddr, "YOUR PASSWORD")
#  text = msg.as_string()
#  server.sendmail(fromaddr, toaddr, text)
#  server.quit()
