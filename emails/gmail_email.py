import smtplib
from email_lv_pwd import gmail_pwd

gmail_user = 'pavan.skt@gmail.com'
gmail_password = gmail_pwd

sent_from = gmail_user
to = ['pavan.skt@gmail.com', 'pavan.soft@gmail.com']
subject = 'Subject'
body = 'Hey, Test'
email_text = """\
From: %s
To: %s
Subject: %s

%s
""" % (sent_from, ", ".join(to), subject, body)

try:
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)
    server.sendmail(sent_from, to, email_text)
    server.close()

    print 'Email sent!'
except:

    print 'Something went wrong...'