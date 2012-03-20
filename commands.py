import argparse,random,string,sys,subprocess
from queries import (Queries,getcon)

from local_settings import *

class DisableUser(argparse.Action):
    '''
    Custom implementation of the argparse Action class used for
    disabling user accounts on a mysql database
    '''

    def __init__(self,option_strings,dest,
                    nargs=None,const=None,
                    default=None,type=None,
                    choices=None,required=False,
                    help=None,metavar=None):
        argparse.Action.__init__(self,
                                option_strings=option_strings,
                                dest=dest,nargs=nargs,const=const,
                                default=default,type=type,choices=choices,
                                required=required,help=help,metavar=metavar)


    def __call__(self, parser, namespace, values, option_string=None):
        db = getcon()
        self.cursor = db.cursor(cursorclass=Queries)
        
        print "Using: "+CONFIG.get('host')
        self.cursor.execute('USE mysql')

        for user in values:
            self.cursor.execute('SELECT user,host FROM user WHERE user = %s', user)
            user_data = self.cursor.fetchall()
            if user_data:
                for row in user_data:
                    answer = raw_input("Are you sure you want to disable " +user+"@"+row.get('host')+" account(Y/n)? ")
                    if answer.lower() in ['y','']:
                        password = self.gen_password()
                        self.cursor.execute("SET PASSWORD FOR '"+row.get('user')+"'@'"+row.get('host')+ "' = PASSWORD('"+password+"')")
                        print "User "+user+"@"+row.get('host')+" password has been reset"
            else:
                print "Skipping... user "+user+" does not exist"
        self.cursor.execute("FLUSH PRIVILEGES")

    def gen_password(self):
        '''
        Generates a random password with letters and numbers in it.
        '''
        ran = random.SystemRandom()
        length = 8
        alpha = string.letters[0:52] + string.digits
        while True:
            password = str().join(ran.choice(alpha) for _ in range(length))
            if set(string.letters[0:52]).intersection(set(password)) \
                and set(string.digits).intersection(set(password)):
                break
        return password

class DisableDb(argparse.Action):

    def __init__(self,option_strings,dest,
                    nargs=None,const=None,
                    default=None,type=None,
                    choices=None,required=False,
                    help=None,metavar=None):
        argparse.Action.__init__(self,
                                option_strings=option_strings,
                                dest=dest,nargs=nargs,const=const,
                                default=default,type=type,choices=choices,
                                required=required,help=help,metavar=metavar)

    def __call__(self,parser,namespace,values,option_string=None):
        db = getcon()
        self.cursor = db.cursor(cursorclass=Queries)
        print "Using: "+CONFIG.get('host')
        self.drop_db(values)

    def backup_db(self,database,backup_dir):
        '''
        Function that backs up a mysql database (wrapper around `mysqldump`)
        '''
        try:
            args = ['mysqldump',database,'--user='+CONFIG['user'],'--host='+CONFIG['host'],'-p'+CONFIG['pass']]
        except KeyError:
            print "One or more settings were not in settings file. exiting..."
            sys.exit(1)
        backup_sql = open(backup_dir+'/'+database+'.sql', 'w')
        return subprocess.call(args,stdout=backup_sql)

    def drop_db(self,databases):
        '''
        Function that drops the given databases in a MySQL database
        '''

        for database in databases:
            self.cursor.execute('SHOW DATABASES LIKE %s', database)
            if self.cursor.fetchall():
                answer = raw_input("(a backup will be created in "+DB_BACKUP_DIR+")\nAre you sure you want to drop "+database+"(Y/n)?")
                if answer.lower() in ['y','']:
                    print "Creating backup at "+DB_BACKUP_DIR+"/"+database+".sql"
                    err_code = self.backup_db(database,DB_BACKUP_DIR)
                    if err_code == 0:
                        self.cursor.execute("DROP DATABASE `"+database+"`")
                        print "Database "+database+" has been deleted"
                    else:
                        print "Problem creating backup for "+database+". Abandoning..."
            else: 
                print "database "+database+" not found"

class Reports(argparse.Action):

    def __init__(self,option_strings,dest,
                    nargs=None,const=None,
                    default=None,type=None,
                    choices=None,required=False,
                    help=None,metavar=None):
        argparse.Action.__init__(self,
                                option_strings=option_strings,
                                dest=dest,nargs=nargs,const=const,
                                default=default,type=type,choices=choices,
                                required=required,help=help,metavar=metavar)

    def __call__(self,parser,namespace,values,option_string=None):
        db = getcon()
        self.cursor = db.cursor(cursorclass=Queries)
        for value in values:
            print value

def add_args():

    parser = argparse.ArgumentParser(description='This is a utility tool for MySQL. It can generate reports as well as perform specific actions on the server.')
    subparsers = parser.add_subparsers()

    parser_disable_user = subparsers.add_parser('disable_user', help="One or more MySQL user accounts to disable.")
    parser_disable_user.add_argument('users',nargs="+",action=DisableUser)

    parser_disable_db = subparsers.add_parser('disable_db', help="One or more databases to back up and delete.")
    parser_disable_db.add_argument('databases', nargs="+",action=DisableDb,
                                    help="One or more MySQL databases to drop and backup")

    parser_reports = subparsers.add_parser('reports', help="Generate reports about MySQL server")
    parser_reports.add_argument('reports', nargs="+",action=Reports,help="Generates a one or more reports about MySQL server")

    return parser


