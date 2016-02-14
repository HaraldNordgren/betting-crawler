#!/usr/bin/env python3

#set pastetoggle=<F2>:q
:
from CodernityDB.database import Database


db = Database('/tmp/tut1')
db.create()

for x in xrange(100):
    print db.insert(dict(x=x))

for curr in db.all('id'):
    print curr
