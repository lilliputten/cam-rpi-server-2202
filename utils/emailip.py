# -*- coding:utf-8 -*-
# @module emailip
# @desc Send ip to email
# @since 2022.02.24, 04:55
# @changed 2022.02.24, 04:58
# See:
# https://www.instructables.com/Raspberry-Pi-Motion-Detection-Security-Camera/

import socket
import smtplib
#  from email.MIMEMultipart import MIMEMultipart
#  from email.MIMEText import MIMEText

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(s.getsockname()[0])
x = s.getsockname()[0]
s.close()

print(x)

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

