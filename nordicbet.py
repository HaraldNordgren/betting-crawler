#!/usr/bin/env python3

import splinter, time, sys, re, json
import pymysql.cursors

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='teams',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

url = 'https://www.nordicbet.com/sv/odds#/#?cat=&reg=&sc=3'
br = splinter.Browser()

br.visit(url)
time.sleep(10)

iframe = br.find_by_xpath("//iframe[@id='SportsbookIFrame']")
br.visit(iframe['src'])
time.sleep(10)

matches = br.find_by_xpath("//div[@ng-repeat='sortedMarket in market']")

teams_pattern = re.compile("(.*) - (.*)")

for match in matches:

    sql_query = "SELECT * FROM matches WHERE "

    event_name = \
            match.find_by_xpath(".//span[@bo-text='data.EventNameDisplay']")

    team_names = event_name.first.value
    #print("%s:" % team_names, end="")

    m = re.match(teams_pattern, team_names)

    if m is None:
        sys.exit(1)

    home_team = m.group(1)
    away_team = m.group(2)
    
    sql_query += "home = '" + home_team + "' "
    sql_query += "AND away ='" + away_team + "';"

    print(" (hej)")

    with connection.cursor() as cursor:
        cursor.execute(sql_query)
        if not cursor.fetchone():

            odds_list = []
            
            for odds in match.find_by_xpath(".//div[@class='ms-mw-row ng-scope']"):
                opt = odds.find_by_xpath(\
                        ".//button[@class='material-button-inner ng-binding']").value
                
                odds_list.append(opt)

                #print(" %s" % opt, end="")
            
            insert_query = "INSERT INTO matches (home, away, odds, site) VALUES('%s', '%s', '%s', 'nordicbet');" % (home_team, away_team, json.dumps(odds_list))
            #print(insert_query)
            
            cursor.execute(insert_query)
            connection.commit()

            print("Added match to database")

