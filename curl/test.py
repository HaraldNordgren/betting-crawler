#!/usr/bin/env python3

import pycurl
from io import BytesIO

buffer = BytesIO()
c = pycurl.Curl()
c.setopt(c.URL, 'https://sport.bethard.com/pagemethods.aspx/GetLeaguesContent')
c.setopt(c.HTTPHEADER, ['RequestTarget: AJAXService'])
c.setopt(c.WRITEDATA, buffer)
c.perform()
c.close()

#curl 'https://sport.bethard.com/pagemethods.aspx/GetLeaguesContent' -H 'RequestTarget: AJAXService' --data 'BranchID=1&LeaguesCollection=19186&showLive=true' --compressed

body = buffer.getvalue()
# Body is a byte string.
# We have to know the encoding in order to print it to a text file
# such as standard output.
print(body.decode('iso-8859-1'))
