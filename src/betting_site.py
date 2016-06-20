#!/usr/bin/env python3

import database
import splinter

class betting_site:

    def print_start_message(self):
        print("\nSCRAPING %s" % self.site.upper())

    def __init__(self):

        self.db = database.match_database()
        self.br = splinter.Browser('chrome')

