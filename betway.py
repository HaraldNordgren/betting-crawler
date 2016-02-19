#!/usr/bin/env python3

import splinter, re, sys, time
from betting_site import betting_site

class betway(betting_site):

    def __init__(self):

        super().__init__()

        self.site = 'Betway'
        self.match_regex = '.*\n(?:.*\n|\s*)(.*) - (.*)\n([0-9.]+)\n([0-9.]+)\n([0-9.]+)'

    def scrape(self):

        url = "https://sports.betway.com/se#/types/3466397537+485674815+1725672712+3268826934+1360997+3507086274+3704679353+3078022958+2870643102+1524192404+1843621643+729817025+4055737068+1820518234+1802141606+1458319990+366154464+1423887585+3102040550+569127004+2746096394+3674556069+3026886452+761515662+813669588+2603733622+2592227149+3602800179+1904582849+3031711876+930117341+338310381+1400761215+3999403102+3328173141+429341966+1087056776+2782025423+3287197706+963501417+1881534845+2669591541+818093756+2152014868+3390411067+3525448603+2663891652+2775370273+2726698235+4037689422+1346358958+2477406238+1048302583+2008947264+2090991074+3137633102+3009078487+2029342244+324223667+3967268438+3036977201+3664293364+3936237159+1760968083+2142016243+568953445+1355916803"

        self.br.visit(url)

        time.sleep(10)

        for oddsbrowser in self.br.find_by_xpath("//table[@class='odds-browser']"):
            
            oddsbrowser.click()
            comp = oddsbrowser.find_by_xpath("./thead/tr").text.split("\n")[1]

            for tr in oddsbrowser.find_by_xpath("./tbody/tr"):

                if tr['class'] == 'header ':
                    if tr.find_by_xpath("./th")[0].text == 'Matchodds':
                        continue
                    else:
                        break

                if tr['class'] == 'date':

                    sql_date = tr.text
                    continue

                m = re.match(self.match_regex, tr.text)
                #print(repr(tr.text))

                if m is None:
                    print("Regex failed: %s" % repr(tr.text))
                    continue

                home_team   = m.group(1)
                away_team   = m.group(2)
                
                odds = {'1': m.group(3), 'X': m.group(4), '2': m.group(5)}
                
                self.db.process_match(comp, home_team, away_team, sql_date, self.site, odds)

        self.br.quit()
