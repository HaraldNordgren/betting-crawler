#!/usr/bin/env python3

import splinter, time, sys, re#, json
import database
import pymysql.cursors

db = database.match_database()

try:
    db.create_table()
except:
    pass

br = splinter.Browser('chrome')

br.visit('https://www.nordicbet.com/sv/odds#/#?cat=&reg=&sc=3')
betting_site = 'nordicbet'
#time.sleep(5)

iframe = br.find_by_xpath("//iframe[@id='SportsbookIFrame']")
br.visit(iframe['src'])
#time.sleep(5)


date_regex      = re.compile(".* ([0-9]+)/([0-9]+)/([0-9]+)\n.*")
teams_pattern   = re.compile("(.*) - (.*)")

for match_date in br.find_by_xpath("//div[@ng-repeat='marketgroup in marketGroups | filter:filterMarketGroups']"):

    date_string = match_date.find_by_xpath(".//div[@class='market-date ng-binding']")[0].text
    m = re.match(date_regex, date_string)

    if m is None:
        sys.exit(1)

    day     = m.group(1)
    month   = m.group(2)
    year    = m.group(3)

    sql_date = "%s-%s-%s" % (year, month, day)

    for match in match_date.find_by_xpath("//div[@ng-repeat='sortedMarket in market']"):

        event_name = match.find_by_xpath(".//span[@bo-text='data.EventNameDisplay']")
        team_names = event_name.first.value
        #print("%s:" % team_names, end="")

        m = re.match(teams_pattern, team_names)

        if m is None:
            sys.exit(1)

        sql_query = "SELECT * FROM matches WHERE "
        
        home_team = m.group(1)
        away_team = m.group(2)
        
        sql_query += "home = '" + home_team + "' "
        sql_query += "AND away ='" + away_team + "' "
        sql_query += "AND date ='" + sql_date + "';"

        db.execute_statement(sql_query)

        if db.fetch_one() is not None:
            continue
        
        odds_list = []
        
        for odds in match.find_by_xpath(".//div[@class='ms-mw-row ng-scope']"):
            
            opt = odds.find_by_xpath(".//button[@class='material-button-inner ng-binding']").value
            odds_list.append(opt)

        #print(sql_date)
        insert_query = "INSERT INTO matches (home, away, date, odds_1, odds_x, odds_2, site) VALUES('%s', '%s', '%s', '%s', '%s', '%s', 'nordicbet');" % (home_team, away_team, sql_date, odds_list[0], odds_list[1], odds_list[2])

        #print(insert_query)
        
        db.execute_statement(insert_query)
        print("Added '%s - %s' %s, %s" % (home_team, away_team, sql_date, betting_site))
