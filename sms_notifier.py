import re
import configparser
import smtplib
from email.message import EmailMessage
import time

class SMSNotifier(object):
    def __init__(self, sms_notifier_config_path):
        self.sms_gateways = {
            "at&t": "txt.att.net",
            "sprint": "messaging.sprintpcs.com",
            "t-mobile": "tmomail.net",
            "verizon": "vtext.com"
        }
        # Pull Configuration and Set Defaults.
        self.config = configparser.ConfigParser()
        self.config.read(sms_notifier_config_path)
        self.email_host = self.config.get('MAIL_SERVER', 'Host',
                                          fallback="smtp.mail.com")
        self.email_port = self.config.get('MAIL_SERVER', 'Port',
                                          fallback=465)
        self.email_username = self.config.get('MAIL_SERVER', 'Username',
                                              fallback="example@mail.com")
        self.email_password = self.config.get('MAIL_SERVER', 'Password',
                                              fallback="examplepassword")

    def __str__(self):
        return f'SMSNotifier Info:\n\
            Host: {self.email_host}:{self.email_port}\n\
                Username: {self.email_username}'

    # TODO: Carrier lookup, phone parsing and sanitization, make not terrible.
    def phone_to_email(self, sms_number, sms_carrier):
        sms_number = re.sub(r'\D', '', sms_number)
        if len(sms_number) != 10:
            sms_number = sms_number[-10:]
        sms_email = sms_number
        sms_email += f'@{self.sms_gateways.get(sms_carrier,"txt.att.net")}'
        return sms_email

    def send_notification(self, sms_number, sms_carrier, subject="", body=""):
        to_email_address = self.phone_to_email(sms_number, sms_carrier)
        msg = EmailMessage()
        msg.set_content(body)
        msg['From'] = self.email_username
        msg['To'] = [to_email_address]
        msg['Subject'] = subject
        print(msg)
        with smtplib.SMTP_SSL(self.email_host, self.email_port) as server:
            server.login(self.email_username, self.email_password)
            server.send_message(msg)


if __name__ == "__main__":
    sn = SMSNotifier("smsnotifier.conf")
