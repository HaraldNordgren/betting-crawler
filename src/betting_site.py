#!/usr/bin/env python3

import database
import splinter

class betting_site:

    def __init__(self):

        self.db = database.match_database()
        self.br = splinter.Browser()

