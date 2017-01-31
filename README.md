# MeetMail
Python script so we do not have to manually write a meetup email each month

## Usage
usage: meetup.py [-h] [-l] [-d] [-e] [-i IN_FILE] [-a ADDITIONAL]
                 [-r REMINDER] [-f FILES]

Using the meetup calendar to generate an email

optional arguments:
-h, --help            show this help message and exit
-l, --limit           Limited to that month only
-d, --dev             Testing purposes
-e, --email           Send email straight to all the people!
-i IN_FILE, --in_file IN_FILE
                      Input file name
-a ADDITIONAL, --additional ADDITIONAL
                      Specify additional meetups manually
-r REMINDER, --reminder REMINDER
                      Name of meetup reminder
-f FILES, --files FILES
                      Specify files to add as attachment

## TODO

[x] Change url and split out to config

[ ] Use other sources as well

[x] Send email from script
