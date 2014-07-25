dbinfo
========================

Requirements
------------
- pymysql
- psycopg2
- docopt

Installation
------------
- Run `python setup.py install`. Best to do it in a virtualenv.
- Create a `~/.dbinfo_config` using the `dbinfo_config.template` and fill it in with your database connection settings

What does this do?
------------------
Run statistics reports for PostgreSQL and MySQL. It writes the output of these reports in csv or json
