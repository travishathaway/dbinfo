import psycopg2
import sys

from .base import Dbinfo


class DbinfoPostgresql(Dbinfo):

    def __init__(self, config):
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

    def usage(self, output_format='csv'):
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

        getattr(self, '_format_%s' % output_format)(report_name='usage')
