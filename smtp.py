import smtplib,subprocess
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

def prompt(prompt):
    data = raw_input(prompt).strip()
    return data

fromaddr = 'sysadmin@supercloud.vn'
toaddrs = ['openemm1000@gmail.com']
password = '123456'
msg = MIMEMultipart()
msg['From']= "sysadmin@supercloud.vn"
msg['To'] = ", ".join(toaddrs)
msg['Subject'] = "Server: mail.longvan.net top 10 sender email"
print "Enter message, end with ^D (Unix) or ^Z (Windows):"

def system_call(command):
    p = subprocess.Popen([command], stdout=subprocess.PIPE, shell=True)
    return p.stdout.read()

# Add the From: and To: headers at the start!
#msg = ("From: %s\r\nTo: %s\r\nSubject: %s\r\n\r\n"
#       % (fromaddr, ", ".join(toaddrs), subject))
#stat_cmd = '''cat /var/opt/axigen/log/everything.txt|grep "connection accepted"|awk '{print $11}'|cut -d "[" -f2 | cut -d "]" -f1|cut -f1 -d:|sort|uniq -c|sort -n|tail -30'''
stat_cmd = '''cat /var/opt/axigen/log/sending.txt|grep "MAIL FROM"|awk '{print $9}'|awk -F '[<>]' '{print $2}'|sort|uniq -c|sort -n|tail -10'''
body = system_call(stat_cmd)

msg.attach(MIMEText(body, 'plain'))
#print "Message length is " + repr(len(msg))
#filename = "hoho.txt"
#attachment = open("hoho.txt", "rb")
 
#part = MIMEBase('application', 'octet-stream')
#part.set_payload((attachment).read())
#encoders.encode_base64(part)
#part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
#msg.attach(part)
 
server = smtplib.SMTP('localhost')
server.login(fromaddr,password)
server.set_debuglevel(1)
server.sendmail(fromaddr, toaddrs, msg.as_string())
server.quit()

