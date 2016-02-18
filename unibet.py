#!/usr/bin/env python3

import urllib.request as request
import json
import database

site = "Unibet"
db = database.match_database()

def scrape_json(url):

    info = json.loads(request.urlopen(url).read().decode())

    for offer in info["betoffers"]:

        if offer["betOfferType"]['id'] != 2:
            continue

        for event in info['events']:
            
            if event["id"] != offer["eventId"]:
                continue

            comp = event["group"]
            sql_date = event["start"].split("T")[0]

            home_team = event['homeName']
            away_team = event['awayName']

            break

        odds = {}

        for outcome in offer['outcomes']:

            raw_odds = str(outcome['odds'])
            float_odds = "%s.%s" % (raw_odds[0], raw_odds[1:])
            
            if outcome['type'] == "OT_ONE":
                odds['odds_1'] = float_odds
            elif outcome['type'] == "OT_CROSS":
                odds['odds_x'] = float_odds
            elif outcome['type'] == "OT_TWO":
                odds['odds_2'] = float_odds

        db.process_match(comp, home_team, away_team, sql_date, site, odds)


url_prefix = "https://e4-api.kambi.com/offering/api/v2/ub/betoffer/group/"
url_suffix = ".json?cat=1295&range_size=100&range_start=0"


leagues = {
        'CL'        : 1000093381,
        'EL'        : 2000051195,
        'Spain'     : 1000461813,
        'Italy'     : 1000461745,
        'Germany'   : 1000461728,
        'France'    : 1000461727,
        'England'   : 1000461733,
        'Sweden'    : 1000461814}


for league_nbr in [2000051195, 1000461733, 1000093381, 1000461814]:

    url = url_prefix + str(league_nbr) + url_suffix
    scrape_json(url)
