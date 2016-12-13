import json
import datetime
import operator
import argparse
import requests
import pyperclip
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import config

today = datetime.datetime.now()
months = []

for i in range(1,13):
    months.append(datetime.date(2016, i, 1).strftime('%B'))

def get_meetups(in_file):
    if in_file is None:
        return requests.get("https://api.meetup.com/self/calendar?photo-host=public&page=20&sig_id=24175662&sig=672eb88f247922fd36ad590603c594acc46f630a").json()
    else:
        with open(in_file, 'r') as meetups:
            return meetups.read()


def generate_email(meetups, args):
    meetups.sort(key=operator.itemgetter('time'))
    subject = "[Meetups] Events for {0}".format(months[today.month-1])
    met = []
    email_body = ""
    if args.reminder:
        email_body += config.email_reminder.format(args.reminder.title())
        meetups = [x for x in meetups if args.reminder.lower() in x['group']['name'].lower()]
    else:
        email_body += config.email_welcome.format(months[today.month-1])
    
    for meetup in meetups:
        date = datetime.datetime.fromtimestamp(meetup['time'] / 1e3)
        meetup['time'] = date
        name = meetup['name']
        if (name not in met and not args.limit) or (name not in met and args.limit and date.month == today.month):
#and not args.limit) and (args.limit and date.month == today.month):
            # add the name and not the meetup to allow different types of meetup from the same groupto be added
            met.append(name)
            email_body = write_meetup(email_body, meetup)

    if args.reminder:
        email_body += config.email_rem_close
        subject = "[Meetups] Reminder for {} on {}".format(args.reminder.title(), meetups[0]['time'])
    else:
        email_body += config.email_close
    if args.output:
        with open(args.output, 'w') as email:
            email.write(email_body)
        print("Meetup email written to: {}".format(args.output))
    return subject, email_body

def write_meetup(email_body, meetup):
    email_body += "\n Name: {} \n".format(meetup['name'])
    email_body += "Meetup: {}\n".format(meetup['group']['name'])
    venue = 'TBC'
    if 'venue' in meetup:
        venue = meetup['venue']['name']
    email_body += "Where: {}\n".format(venue)
    email_body += "When: {}\n".format(meetup['time'])
    email_body += "Link: {}\n".format(meetup['link'])
    email_body += '\n ----- \n'
    return email_body

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Using the meetup calendar to generate an email')
    parser.add_argument('-l', '--limit', help='Limited to that month only', required=False, action="store_true")
    parser.add_argument('-d', '--dev', help='Testing purposes', required=False, action="store_true")
    parser.add_argument('-e', '--email', help='Send email straight to all the people!', required=False, action="store_true")
    parser.add_argument('-i','--in_file', help='Input file name',required=False)
    parser.add_argument('-o','--output',help='Output file name', required=False)
    parser.add_argument('-r','--reminder',help='Name of meetup reminder', required=False)
    args = parser.parse_args()
    meetups = get_meetups(args.in_file)
    if not args.in_file:
        subject, body  = generate_email(meetups, args)
    else:
        body = meetups
    print(subject)
    print(body)
    if args.email and "y" in input("ready to send?").lower():
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = config.uname 
        if args.dev:
            msg['To'] = ", ".join(config.recs_dev)
        else:
            msg['To'] = ", ".join(config.recs)
        mail = smtplib.SMTP('outlook.office365.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(config.uname, config.pwd)
        to_addr = config.bcc 
        to_addr += config.recs if not args.dev else config.recs_dev
        print("Sending to: {}".format(to_addr))
        print(mail.sendmail(config.uname, to, msg.as_string()))
        print("email sent")
