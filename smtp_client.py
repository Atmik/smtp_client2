# -*- coding: utf-8 -*-

import smtplib
import argparse
import socket

parser = argparse.ArgumentParser(add_help = True, description = 'Simple SMTP client')
parser.add_argument('-s', '--server', required = True, help = 'SMTP server host')
parser.add_argument('-p', '--port', required = True, help = 'SMTP server port')
parser.add_argument('-u', '--username', required = True, help = 'Username for SMTP server')
parser.add_argument('-P', '--password', required = True, help = 'Password for SMTP server')
parser.add_argument('-m', '--message', required = True, help = 'Message in HTML')
parser.add_argument('-f', '--fromSen', required = False, help = 'Sender field')
parser.add_argument('-e', '--emails', required = True, help = 'Receivers list')
args = parser.parse_args()

if args.fromSen is None:
    args.fromSen = args.username

def prepare_mail_list():
    try:
        emails = open(args.emails, 'r')
    except IOError:
        raise SystemExit('[FATAL] Wrong path to emails file')
    receivers = []
    for email in emails.readlines():
        email = email.rstrip('\n')
        receivers.append(email)
        for mail in receivers:
            mail.replace(' ', '')
    return receivers

def prepare_message():
    try:
        message = open(args.message, 'r')
        msg = message.read() # Check what we can do with blank lines
        return msg
    except IOError:
        raise SystemExit('[FATAL] Wrong path to message file')

def main():
    try:
        print 'Hello'
        smtpClient = smtplib.SMTP(args.server, args.port)
        print 'Starting SMTP TLS'
        smtpClient.starttls()
        smtpClient.login(args.username, args.password)
        print 'Login successfull!'
        to_list = prepare_mail_list()
        print to_list
        for mail in to_list:
            print 'Sending mail from %s to %s.' % (args.username, mail)
            smtpClient.sendmail(args.fromSen, mail, prepare_message())

        smtpClient.close()
        print 'Success!'
    except (socket.error, smtplib.SMTPException), e:
        errcode = getattr(e, 'smtp_code', -1)
        errmsg = getattr(e, 'smtp_error', 'ignore')
        print errcode 
        print errmsg

if __name__ == '__main__':
    main()