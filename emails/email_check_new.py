import base64
import json
import logging
import os
import traceback
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import requests

sender = 'smpradeepk2@hexaware.com'
password = 'Nove@2020'
receivers = ['jignashreddyy@hexaware.com']
msg = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test
This is a test e-mail message.
"""
try:
    print("*********")
    server1 = smtplib.SMTP('smtp.office365.com', 587)
    print("*********")
    print(server1)
    server1.ehlo()
    server1.starttls()
    server1.login('40910@hexaware.com', 'Nove@2020')
    server1.sendmail('40910@hexaware.com', '42952@hexaware.com', "helll world")
    print("Successfully sent email")
except Exception as e:
    import traceback

    print(traceback.format_exc())
    print("Error: unable to send email" + str(e))





