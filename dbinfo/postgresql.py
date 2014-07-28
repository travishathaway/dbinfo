import psycopg2
import sys

from .base import Dbinfo


class DbinfoPostgresql(Dbinfo):

    '''
    PostgreSQL implementation of Dbinfo.  Class methods represent report types.
    '''

    def __init__(self, config, outfile=None):
        '''
        Using config, attempt to create a database connection and store the
        cursor on self.
        '''

        self.outfile = outfile

        try:
            conn = psycopg2.connect(
                host=config['host'],
                port=config.get('port', 5432),
                user=config.get('user', 'postgres'),
                password=config.get('pass', ''),
                dbname='postgres'
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

        self.cur.execute(
            '''
            SELECT
                datname,
                round(
                    pg_database_size(datname)/1024.0/1024.0,
                    2
                )AS size_in_mb
            FROM pg_database
            WHERE datistemplate =false;
            '''
        )

        getattr(self, '_format_%s' % output_format)(
            headers=['Database', 'Size in MB'])

    def users(self, output_format='csv'):

        self.cur.execute(
            '''
            SELECT u.usename AS "User name",
            CASE WHEN u.usesuper AND u.usecreatedb THEN CAST('superuser, create
            database' AS pg_catalog.text)
                WHEN u.usesuper THEN CAST('superuser' AS pg_catalog.text)
                WHEN u.usecreatedb THEN CAST('create database' AS
            pg_catalog.text)
                ELSE CAST('' AS pg_catalog.text)
            END AS "Attributes"
            FROM pg_catalog.pg_user u
            ORDER BY 1;
            '''
        )

        getattr(self, '_format_%s' % output_format)(
            headers=['User', 'Attributes'])
