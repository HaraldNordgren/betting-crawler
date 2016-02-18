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

        comp = match['scn']

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


for i in range(10):

    url = "https://sbsitefacade.bpsgameserver.com/isa/v2/902/sv/event?betgroupgroupingids=36&eventPhase=1&marketCount=50&page=%d&subCategoryIds=6134,2612,1,108,489,488,4309,113,110,117,1701,116,109,120,7954,1609,1363,8738,3,7,148,4,5,6,8,12,13,5949,9,11,10,15,16,1884,122,3016,2275,2350,43,2238,138,5611,9479,1439,1440,1441,1438,5319,5320,3506,158,5469,19,126,20,25,398,1415,251,128,129,130,131,132,133,734,3413,3427,3423,6081,6054,23,595,1549,41,1239,11374,33,3137,275,29,30,31,32,26,163,35,27,283,634,151,28,45" % (i+1)

    print (i+1)
    
    scrape_json(url)

