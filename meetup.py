import config
import argparse
from meetapi import MeetApi
from mailer import MeetMail

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Using the meetup calendar to generate an email')
    parser.add_argument('-l', '--limit', help='Limited to that month only', required=False, action="store_true")
    parser.add_argument('-d', '--dev', help='Testing purposes', required=False, action="store_true")
    parser.add_argument('-e', '--email', help='Send email straight to all the people!', required=False, action="store_true")
    parser.add_argument('-i','--in_file', help='Input file name',required=False)
    parser.add_argument('-a', '--additional', help='Specify additional meetups manually', required=False)
    parser.add_argument('-r','--reminder',help='Name of meetup reminder', required=False)
    parser.add_argument('-f', '--files', help='Specify files to add as attachment', required=False, action="append")
    args = parser.parse_args()

    MA = MeetApi(reminder=args.reminder, limit=args.limit, in_file=args.in_file)
    MSG = config.email_reminder.format(args.reminder) if args.reminder else config.email_welcome.format(MA.months[MA.today.month-1])
    SUB, MEETUPS = MA.gen_meetups()
    # add in additional hard coded meetups if necessary
    # - this ruins date sorting, but...
    if args.additional:
        with open(args.additional, 'r') as input_file:
            MEETUPS += input_file.read()

    MSG += MEETUPS
    MSG += config.email_rem_close if args.reminder else config.email_close

    mailer = MeetMail(config.uname, config.pwd, config.smtp_server, config.smtp_port)

    if args.dev:
        send_to = config.recs_dev
    else:
        send_to = config.recs + config.bcc

    if args.dev and not args.email:
        print(MSG)

    if args.email:
        if args.files:
            mailer.send(config.uname, send_to, SUB, MSG, args.files)
        else:
            mailer.send(config.uname, send_to, SUB, MSG)
