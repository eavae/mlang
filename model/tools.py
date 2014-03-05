#coding:utf-8
import re
import hashlib
from const import I18n
from email.mime.text import MIMEText
import smtplib

class QQMail(object ):
    def __init__ (self ,account,password): 
        self.account="%s@qq.com" %account
        self.password=password

    def send(self,to,title,content):
        print self.account,self.password
        server = smtplib.SMTP('smtp.qq.com' )
        server.login(self.account,self.password)

        msg = MIMEText(content)
        msg['Content-Type' ]='text/html;charset="utf-8"'
        msg['Subject' ] = title
        msg['From' ] = self.account
        msg['To' ] = to
        server.sendmail(self.account, to,msg.as_string())
        server.close()

def validate_email(email):
    if re.match("^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$", email) != None:
        return True
    return False

def pack_password(password):
    return hashlib.md5(password).hexdigest()

def vali_nickname(nickname):
    if len(nickname) > 0 and len(nickname) < 40:
        return True
    return False
def langName(lang):
    if I18n.LANG.has_key(lang):
        return I18n.LANG[lang]
    else:
        return None

def main():
    pass

if __name__ == '__main__':
    main()