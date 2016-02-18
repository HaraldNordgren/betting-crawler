#!/usr/bin/env python3

import urllib.request as request
import json
import database

db = database.match_database()

site = "Unibet"

resp = request.urlopen("https://e3-api.kambi.com/offering/api/v2/ub/betoffer/group/1000094985.json?cat=1295&market=se&lang=sv_SE&range_size=100&range_start=0&suppress_response_codes&channel_id=1")
j = json.loads(resp.read().decode())

for offer in j["betoffers"]:
    if offer["betOfferType"]['id'] == 2:

        for event in j['events']:
            if event["id"] == offer["eventId"]:

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
