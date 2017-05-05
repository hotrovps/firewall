import smtplib,subprocess,yaml
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

with open("config.yaml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

def smtp(subject,body):
	fromaddr = cfg['smtp']['sender']
	toaddrs = cfg['smtp']['receiver']
	password = cfg['smtp']['pass']
	host = cfg['smtp']['host']
	msg = MIMEMultipart()
	msg['From']= fromaddr
	msg['To'] = ", ".join(toaddrs)
	msg['Subject'] = subject
	body = body
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP(host)
	server.login(fromaddr,password)
	server.set_debuglevel(1)
	server.sendmail(fromaddr, toaddrs, msg.as_string())
	server.quit()
