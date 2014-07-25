import pymysql
import sys

from .base import Dbinfo


class DbinfoMysql(Dbinfo):

    '''
    MySQL implementation of Dbinfo.  Class methods represent report types.
    '''

    def __init__(self, config):
        '''
        Using config, attempt to create a database connection and store the
        cursor on self.
        '''

        try:
            conn = pymysql.connect(
                host=config['host'],
                port=config.get('port', 3306),
                user=config.get('user', 'root'),
                passwd=config.get('pass', ''),
                db='mysql'
            )

            self.cur = conn.cursor()
        except(KeyError):
            sys.stdout.write(
                'You must define "host", "user", and "pass" in config\n'
            )
            sys.exit(1)

    def disk_usage(self, output_format='csv'):
        '''
        Disk usage per database
        '''

        self.cur.execute('USE information_schema')
        self.cur.execute('''
            SELECT table_schema 'database',
            round(
                sum( data_length + index_length ) / ( 1024 * 1024 ) , 2
            ) size
            FROM information_schema.TABLES
            GROUP BY table_schema
        ''')

        getattr(self, '_format_%s' % output_format)(
            report_name='usage', headers=['Database', 'Size in MB'])
