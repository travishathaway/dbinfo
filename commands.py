import argparse


class UserAction(argparse.Action):
    '''
    Custom implementation of the argparse Action class
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
                                required=required,help=help,metavar=metavar,)

    def __call__(self, parser, namespace, values, option_string=None):
        print values



def add_args():

    parser = argparse.ArgumentParser(description='This is a utility tool for MySQL. It can generate reports as well as perform specific actions on the server.')

    parser.add_argument('--user', '-u', nargs="+",action=UserAction,
                        type=str, help="One or more MySQL user accounts to disable.")
    parser.add_argument('--database', '-d', nargs="+",type=str, help="One or more MySQL databases to drop. These databases will backed up to the ARC back dir.")

    parser.add_argument('--report', '-r', nargs="+",type=str, help="Please specify a report to generate.")

    return parser


