#!/usr/bin/env python3

import splinter, re, sys
from betting_site import betting_site

class betway(betting_site):

    def __init__(self):

        super().__init__()

        self.site = 'Betway'
        self.match_regex = '.*\n .*\n(.*) - (.*)\n([0-9.]+)\n([0-9.]+)\n([0-9.]+)'

    def scrape(self):

        self.br.visit('https://sports.betway.com/se#/soccer/england/premier-league')
        comp = "Premier League"

        for tr in self.br.find_by_xpath("//tbody[@class='oddsbody']").find_by_xpath("./tr"):

            if tr['class'] == 'date':

                sql_date = tr.text
                continue

            if tr['class'] == 'header ':
                
                if tr.text == 'Vinnare':
                    break
                else:
                    continue

            m = re.match(self.match_regex, tr.text)

            if m is None:
                print("Regex failed")
                sys.exit(1)

            home_team   = m.group(1)
            away_team   = m.group(2)
            
            odds = {'1': m.group(3), 'X': m.group(4), '2': m.group(5)}
            
            self.db.process_match(comp, home_team, away_team, sql_date, self.site, odds)

        self.br.quit()
