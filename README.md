This program generates reports about your MySQL databases and also preforms actions (like disabling users and dropping databases).  It is my intention that you will first generate a report and then come to the conclusion that some kind of action must happen.  Well then, if these are your intentions than this may be your cup of joe.

### Requirements:
    - Need Admin MySQL account
    - Python-mysqldb installed
    - Atleast Python2.7 (if not just make sure to install argparse module)
    - Database full of old crap

### Instructions
    - Fill out the settings.py file and change the name to local_settings.py.  Make sure no one can read this file!!!
    - run the manage.py command with one of the sub commands (e.g. python manage.py disable_users user1 user2 user3)

That's it for now!
