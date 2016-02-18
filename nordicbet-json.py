#!/usr/bin/env python3

import urllib.request as request
import json
import database

site = "Nordicbet"
db = database.match_database()

def scrape_json(url):

    info = json.loads(request.urlopen(url).read().decode())

    for match in info['el']:

        sql_date = match['ml'][0]['dd'].split("T")[0]
        home_team = match['epl'][0]['pn']
        away_team = match['epl'][1]['pn']

        comp = match['rn']

        odds = {}

        for msl in match['ml'][0]['msl']:
            if msl['mst'] == '1':
                odds['odds_1'] = msl['msp']
            elif msl['mst'] == 'X':
                odds['odds_x'] = msl['msp']
            elif msl['mst'] == '2':
                odds['odds_2'] = msl['msp']
        
        #print("%s %s %s - %s %s" % (comp, date, home_team, away_team, str(odds)))
        db.process_match(comp, home_team, away_team, sql_date, site, odds)



leagues = { 'spain': {'group': "36", 'page': "1", 'cats': "12,13"} }

for l in leagues:

    league = leagues[l]
    
    url = "https://sbsitefacade.bpsgameserver.com/isa/v2/902/sv/event"
    url += "?betgroupgroupingids=%s&page=%s&subCategoryIds=%s" % (league['group'], league['page'], league['cats'])
    
    scrape_json(url)
