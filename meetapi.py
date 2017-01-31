import requests
import operator
import datetime
import config

class MeetApi:

    def __init__(self, in_file = None, limit = False, reminder = None):
        self.file = in_file
        self.meetups = self.get_meetups(in_file)
        self.months = []
        self.today = datetime.datetime.now()
        self.limit = limit
        self.reminder = reminder
        for i in range(1,13):
            self.months.append(datetime.date(2016, i, 1).strftime('%B'))


    def get_meetups(self, in_file):
        if in_file is None:
            return requests.get("https://api.meetup.com/self/calendar?photo-host=public&page=20&sig_id=24175662&sig=672eb88f247922fd36ad590603c594acc46f630a").json()
        else:
            with open(in_file, 'r') as meetups:
                return meetups.read()

    def gen_meetups(self):
        self.meetups.sort(key=operator.itemgetter('time'))
        self.msg = ""
        met = []
        self.subject = "[Meetups] Events for {0}".format(self.months[self.today.month-1])
        if self.reminder:
            self.meetups = [x for x in self.meetups if self.reminder.lower() in x['group']['name'].lower()]
            self.subject = "[Meetups] Reminder for {} on {}".format(self.reminder.title(), self.meetups[0]['time'])
        for meetup in self.meetups:
            date = datetime.datetime.fromtimestamp(meetup['time'] / 1e3)
            meetup['time'] = date
            name = meetup['name']
            if (name not in met and not self.limit) or (name not in met and self.limit and date.month == self.today.month):
                # add the name and not the meetup to allow different types of meetup from the same groupto be added
                met.append(name)
                self.add_meetup(meetup)
        return (self.subject, self.msg)

    def add_meetup(self, meetup):
        email_body = "\nName: {} \n".format(meetup['name'])
        email_body += "Meetup: {}\n".format(meetup['group']['name'])
        venue = 'TBC'
        if 'venue' in meetup:
            venue = meetup['venue']['name']
        email_body += "Where: {}\n".format(venue)
        email_body += "When: {}\n".format(meetup['time'])
        email_body += "Link: {}\n".format(meetup['link'])
        email_body += '\n ----- \n'
        self.msg += email_body

if __name__ == "__main__":
    ma = MeetApi()
    print(ma.gen_meetups())
