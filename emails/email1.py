import smtplib
from email_lv_pwd import pwd

# Creating SMTP Client Session
imap_server = "imap-mail.outlook.com"
imap_port = 993
smtp_server = "smtp.gmail.com" #"smtp-mail.outlook.com"
smtp_port = 587

smtpobj = smtplib.SMTP('whyexch-prod-vip-smtp-mailhost', 25)
# start TLS for security which makes the connection more secure
smtpobj.starttls()
senderemail_id="pavankumar.kota@lv.com"
senderemail_id_password= pwd
receiveremail_id= senderemail_id
# Authentication for signing to gmail account
smtpobj.login(senderemail_id, senderemail_id_password)
# message to be sent
message = "Hey this is the test code for sending email from my account to my account"
# sending the mail - passing 3 arguments i.e sender address, receiver address and the message
smtpobj.sendmail(senderemail_id,receiveremail_id, message)
# Hereby terminate the session
smtpobj.quit()
print "mail send - Using simple text message"