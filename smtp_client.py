# -*- coding: utf-8 -*-

import smtplib
import socket
import ConfigParser
import shutil
import base64
import tempfile

config = ConfigParser.RawConfigParser()
config.read('configs.conf')

server = config.get('Server', 'server')
port = config.getint('Server', 'port')
username = config.get('Server', 'username')
password = config.get('Server', 'password')
message = config.get('Server', 'message')
fromSen = config.get('Server', 'fromSen')
emails = config.get('Server', 'emails')
track = config.getboolean('Server', 'track')
trackURL = config.get('Server', 'trackingHandler')

if fromSen is None:
    fromSen = username

def prepare_mail_list(f):
    try:
        emails = open(f, 'r')
    except IOError:
        raise SystemExit('[FATAL] Wrong path to emails file')
    receivers = []
    for email in emails.readlines():
        email = email.rstrip('\n')
        receivers.append(email)
        for mail in receivers:
            mail.replace(' ', '')
    return receivers

def prepare_message(mes, t, mail):
    if t:
        try:
            with open(mes) as msg:
                html = msg.readlines()
                injection = '<img alt="" src="%suser=%s" width="1" height="1" border="0" />' % (trackURL, base64.b64encode(mail))
                html_list = []

                for line in html:
                    html_list.append(line)

                html_list.insert(-2, injection)
                tmp_file = str(mes+'.tmp')
                shutil.copy(mes, tmp_file)

                with open(tmp_file, 'r+') as tmp:
                    for line in html_list:
                        tmp.writelines('\n'+line)
                    return tmp.read()   #  Returning raw text
        except Exception:
            print Exception
    else:
        try:
            with open(m, 'r') as message:
                msg = message.read()
                return msg
        except IOError:
            raise SystemExit('[FATAL] Wrong path to message file')

def main():

    try:
        smtpClient = smtplib.SMTP(server, port)
        print 'Starting SMTP TLS'
        smtpClient.starttls()

        if smtpClient.login(username, password): # Trying to login to the server
            print "Login successfull!"
        elif Exception:
            print Exception

        to_list = prepare_mail_list(emails)
        print to_list

        for mail in to_list:
            print 'Sending mail from %s to %s.' % (username, mail)
            smtpClient.sendmail(fromSen, mail, prepare_message(message, track, mail))

        smtpClient.close()
        print 'Success!'

    except (socket.error, smtplib.SMTPException), e:
        errcode = getattr(e, 'smtp_code', -1)
        errmsg = getattr(e, 'smtp_error', 'ignore')
        print errcode 
        print errmsg

if __name__ == '__main__':
    main()
