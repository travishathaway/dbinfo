import subprocess, random, string,sys
from MySQLdb.cursors import DictCursor
from MySQLdb import connect

try:
    from local_settings import *
except ImportError, e:
    print "could not find settings file. Exiting..."
    sys.exit(0)


def getcon(config=CONFIG):
    '''
    Function that reads the settings file and establishes database connection
    '''
    try:
        return connect(user=config['user'],passwd=config['pass'],host=config['host'])
    except KeyError, e:
        print "You need to fill out the settings file"
        sys.exit(1)

class Queries(DictCursor):
    '''
    Queries is a subclass of the MySQLdb.cursors.DictCursor class.
    It is meant to hold queries used in the application
    '''

    def db_info(self):
       self.execute('USE information_schema')
       self.execute('''SELECT table_schema 'database', 
                        round( sum( data_length + index_length ) / ( 1024 *1024 ) , 2 ) size 
                        FROM information_schema.TABLES 
                        GROUP BY table_schema''')


