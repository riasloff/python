import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

LOGIN_MAIL = (os.environ['LOGIN_MAIL'])
PASSWORD_MAIL = (os.environ['PASSWORD_MAIL'])

def main():
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.ehlo()
  server.starttls()
  server.login(LOGIN_MAIL, PASSWORD_MAIL)
  print('Login OK')
  action = 0
  while action < 1 or action > 2:
    action = int(input('1. Create\n2. Delete\n'))

  vpn_user = input('Enter vpn username\n')
  if action == 1:
    action = 'create'
  else:
    action = 'delete'
  request = f'{action} {vpn_user}'
  msg = MIMEMultipart()

  text_part = MIMEText(request)
  msg['Subject'] = '[VPN] Manage users'
  msg['From'] = LOGIN_MAIL
  msg['To'] = 'vpn@example.com'
  msg.attach(text_part)
  server.sendmail(LOGIN_MAIL, 'vpn@example.com', msg.as_string())
  server.quit()


if __name__ == '__main__':
  main()