# -*- coding: utf-8 -*-
# (c) 2012 Niko Böckerman <niko.bockerman@gmail.com>
# Released under the terms of the 2-clause BSD license.


import smtplib
from email.mime.text import MIMEText

#import settings


class Emailing:
    '''
    classdocs
    '''
    def __init__(self, fromAddr,  toAddr,  host,  useSsl,  username="",  password=""):
        '''
        Constructor
        '''
        self.fromAddr = fromAddr
        self.toAddr = toAddr
        self.host = host
        self.useSsl = useSsl
        self.username = username
        self.password = password
        self.login = False
        if username != "" and password != "":
            self.login = True
    
    def sendmail(self, subject, message):
        msg=MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.fromAddr
        msg['To'] = self.toAddr
        try:
            if self.useSsl:
                smtp = smtplib.SMTP_SSL(host=self.host)
            else:
                smtp = smtplib.SMTP(host=self.host)
            if self.login:
                smtp.login(self.username,  self.password)
            smtp.send_message(msg)
        except Exception as e:
            print("Exception caught while sending message:")
            print(e)
