import smtplib,subprocess
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

def prompt(prompt):
    data = raw_input(prompt).strip()
    return data

fromaddr = 'sysadmin@abc.us'
toaddrs = ['huyvu@gmail.com']
password = '123456'
msg = MIMEMultipart()
msg['From']= "sysadminabc.us"
msg['To'] = ", ".join(toaddrs)
msg['Subject'] = "Email from Python"
print "Enter message, end with ^D (Unix) or ^Z (Windows):"

def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    return p.stdout.read()

# Add the From: and To: headers at the start!
#msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
#       % (fromaddr, ", ".join(toaddrs), subject))
stat_cmd = '''cat /var/opt/email/sending.txt|grep "MAIL FROM"|awk '{print $9}'|awk -F '[<>]' '{print $2}'|sort|uniq -c|sort -n|tail -10'''
body = system_call(stat_cmd)

msg.attach(MIMEText(body, 'plain'))
 
server = smtplib.SMTP('localhost')
server.login(fromaddr,password)
server.set_debuglevel(1)
server.sendmail(fromaddr, toaddrs, msg.as_string())
server.quit()

