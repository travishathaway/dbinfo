#! /usr/bin/env python
'''
Usage:
    dbinfo <report> [-d <dbms> -f <format> -o <outfile>]

Options:
    -h --help  Show this screen.
    -d <dbms>, --dbms <dbms>  Database Engine [default: mysql]
    -f <format>, --format <format>  Database Engine [default: csv]
    -o <outfile>, --outfile <outfile>  Output filename
'''
import ConfigParser
import os
import sys
from docopt import docopt


def load_config():
    config = ConfigParser.RawConfigParser(allow_no_value=True)
    db_settings = {}
    try:
        config.readfp(open('%s/.dbinfo_config' % os.environ['HOME']))
        for section in config.sections():
            db_settings[section] = {}
            for params in config.items(section):
                db_settings[section][params[0]] = params[1]
    except (IOError):
        sys.stdout.write('You have no config file: ~/.dbinfo_config\n')
        sys.stdout.write('Please create it\n')

    return db_settings


def main():
    args = docopt(__doc__, version='dbinfo 0.1')
    db_settings = load_config()

    if args['--dbms'] == 'mysql':
        from .mysql import DbinfoMysql
        dbinfo = DbinfoMysql(db_settings['mysql'],
                             outfile=args.get('--outfile'))

    elif args['--dbms'] == 'postgresql':
        from .postgresql import DbinfoPostgresql
        dbinfo = DbinfoPostgresql(db_settings['postgresql'],
                                  outfile=args.get('--outfile'))

    else:
        sys.stdout.write(
            'Unrecognized DBMS "%s"\n' % args['--dbms']
        )
        sys.exit(1)

    try:
        getattr(dbinfo, args['<report>'])(output_format=args['--format'])
    except(AttributeError):
        sys.stdout.write(
            'Report "%s" is not a valid report type\n' % args['<report>']
        )
        sys.exit(1)


if __name__ == '__main__':
    main()
