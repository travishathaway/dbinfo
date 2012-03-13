#! /usr/bin/env python 


import queries,commands


db = queries.getcon()
c = queries.Queries(db)


parser = commands.add_args()
args = parser.parse_args()

#c.db_info()

#print c.fetchall()
