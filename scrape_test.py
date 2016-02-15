#!/usr/bin/env python3

from nordicbet import nordicbet
from betway import betway

n = nordicbet()
n.scrape()

b = betway()
b.scrape()
