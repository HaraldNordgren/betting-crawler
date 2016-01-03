#!/usr/bin/env python3

import splinter, time, sys

url = 'https://www.nordicbet.com/sv/odds#/#?cat=&reg=&sc=3'
br = splinter.Browser()

br.visit(url)
time.sleep(10)

iframe = br.find_by_xpath("//iframe[@id='SportsbookIFrame']")
br.visit(iframe['src'])
time.sleep(10)

matches = br.find_by_xpath("//div[@ng-repeat='sortedMarket in market']")

for match in matches:

    event_name = \
            match.find_by_xpath(".//span[@bo-text='data.EventNameDisplay']")
    print("%s:" % event_name.first.value, end="")
    
    for odds in match.find_by_xpath(".//div[@class='ms-mw-row ng-scope']"):
        opt = odds.find_by_xpath(\
                ".//button[@class='material-button-inner ng-binding']").value
        print(" %s" % opt, end="")
    
    print()

print()
