import smtplib
from email.mime.text import MIMEText


class sender():
    def __init__(self, mailTitle, mailFrom, mailFromPwd, mailTo):
        self.mailTitle = mailTitle
        self.mailFrom = mailFrom
        self.mailFromPwd = mailFromPwd
        self.mailTo = mailTo

    def send(self, content):
        msg = MIMEText(content)
        msg["Subject"] = self.mailTitle
        msg["From"] = self.mailFrom
        msg["To"] = self.mailTo

        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(self.mailFrom, self.mailFromPwd)
        server.send_message(msg)
        server.quit()
