#!/usr/bin/env python3

import splinter, time, sys, re
from betting_site import betting_site

class nordicbet(betting_site):
    
    def __init__(self):

        super().__init__()

        self.site = 'Nordicbet'

    def scrape(self):

        self.br.visit('https://www.nordicbet.com/sv/odds#/#?cat=&reg=&sc=3')
        comp = "Premier League"

        iframe = self.br.find_by_xpath("//iframe[@id='SportsbookIFrame']")
        self.br.visit(iframe['src'])

        date_regex      = re.compile(".* ([0-9]+)/([0-9]+)/([0-9]+)\n.*")
        teams_pattern   = re.compile("(.*) - (.*)")

        for match_date in self.br.find_by_xpath(
                "//div[@ng-repeat='marketgroup in marketGroups | filter:filterMarketGroups']"):

            date_string = match_date.find_by_xpath(".//div[@class='market-date ng-binding']")[0].text
            m = re.match(date_regex, date_string)

            if m is None:
                sys.exit(1)

            day     = m.group(1)
            month   = m.group(2)
            year    = m.group(3)

            sql_date = "%s-%s-%s" % (year, month, day)

            for match in match_date.find_by_xpath(".//div[@ng-repeat='sortedMarket in market']"):

                event_name = match.find_by_xpath(".//span[@bo-text='data.EventNameDisplay']")
                team_names = event_name.first.value

                m = re.match(teams_pattern, team_names)

                if m is None:
                    sys.exit(1)

                home_team = m.group(1)
                away_team = m.group(2)
                
                odds = {}
                
                for (col, odds_data) in zip(self.db.odds_cols, match.find_by_xpath(
                    ".//div[@class='ms-mw-row ng-scope']")):
                    
                    odds[col] = odds_data.find_by_xpath(
                            ".//button[@class='material-button-inner ng-binding']").value

                self.db.process_match(comp, home_team, away_team, sql_date, self.site, odds)

        self.br.quit()
