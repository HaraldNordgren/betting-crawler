#!/usr/bin/env python3

import pymysql, sys
from decimal import Decimal
from teams import teams

debug = True

MYSQL_UNKNOWN_DATABASE  = 1049
MYSQL_TABLE_EXISTS      = 1050

class match_database:

    def create_database(self):

        db = pymysql.connect(host="localhost", user="root")
        db.cursor().execute('CREATE DATABASE %s;' % self.database_name)
        db.commit()
        db.close()

    def connect(self):
        self.connection = pymysql.connect(host='localhost', user='root', password='', db=self.database_name, 
                charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

    def create_table(self):

        precision = 5
        decimals = 3

        statement = "CREATE TABLE %s (competition VARCHAR(30), home VARCHAR(20), " % self.matches_table
        statement += "away VARCHAR(20), date DATE, "
        statement += "odds_1 DECIMAL(%d,%d), " % (precision, decimals)
        statement += "odds_x DECIMAL(%d,%d), " % (precision, decimals)
        statement += "odds_2 DECIMAL(%d,%d), " % (precision, decimals)
        statement += "site VARCHAR(50));"

        self.execute(statement)

    def __init__(self):

        self.log = open('.database_log.txt', 'a')
        
        self.database_name = "odds_data"
        self.matches_table = "matches"

        try:
            self.connect()

        except pymysql.err.InternalError as e:
            if e.args[0] != MYSQL_UNKNOWN_DATABASE:
                raise e

            self.create_database()
            self.connect()

        self.cursor = self.connection.cursor()

        try:
            self.create_table()
        
        except pymysql.err.InternalError as e:
            if e.args[0] != MYSQL_TABLE_EXISTS:
                raise e
        
        self.odds_cols  = ['odds_1', 'odds_x', 'odds_2']
        self.teams      = teams()

    def execute(self, statement, commit=True):
        
        self.log.write("%s\n\n" % statement)
        self.cursor.execute(statement)

        if commit:
            self.connection.commit()

    def insert_match(self, comp, home_team, away_team, sql_date, site, odds):

        insert_query = "INSERT INTO matches (competition, home, away, date, odds_1, odds_x, odds_2, site) "
        insert_query += "VALUES('%s', '%s', '%s', '%s', " % (comp, home_team, away_team, sql_date)
        insert_query += "'%s', '%s', '%s', '%s');" % (odds['odds_1'], odds['odds_x'], odds['odds_2'], site)
        
        self.execute(insert_query)
        print("Added %s: '%s - %s' %s, %s" % (comp, home_team, away_team, sql_date, site))

    def update_odds(self, comp, home_team, away_team, sql_date, site, new_odds, old_odds):
       
        changed_odds = {}

        for col in self.odds_cols:
            if Decimal(new_odds[col]) != old_odds[col]:
                changed_odds[col] = Decimal(new_odds[col]) - old_odds[col]

        if not changed_odds:
            return

        print("Updated %s: %s - %s, %s, %s" % (comp, home_team, away_team, sql_date, site))

        pairs = []
        
        for col in changed_odds:
            print("%s: %s -> %s (%s)" % (col, old_odds[col], new_odds[col], changed_odds[col]))
            pairs.append("%s='%s'" % (col, new_odds[col]))
        
        print()

        statement = "UPDATE %s SET " % self.matches_table
        statement += ",".join(pairs)

        statement += " WHERE competition = '" + comp
        statement += "' AND home = '" + home_team
        statement += "' AND away ='" + away_team
        statement += "' AND site ='" + site
        statement += "' AND date ='" + sql_date + "';"

        self.execute(statement)

    def process_match(self, comp, home_team, away_team, sql_date, site, odds):

        home_team = self.teams.get_synonym(home_team)
        away_team = self.teams.get_synonym(away_team)
        
        sql_query = "SELECT * FROM matches WHERE "
        sql_query += "competition = '" + comp
        sql_query += "' AND home = '" + home_team
        sql_query += "' AND away ='" + away_team
        sql_query += "' AND site ='" + site
        sql_query += "' AND date ='" + sql_date + "';"

        self.execute(sql_query, commit=False)
        
        match = self.cursor.fetchone()

        if match is None:
            self.insert_match(comp, home_team, away_team, sql_date, site, odds)
            return
        
        old_odds = {col: match[col] for col in self.odds_cols}
        self.update_odds(comp, home_team, away_team, sql_date, site, odds, old_odds)

    def find_arbitrages(self):

        find_duplicates_statement = "SELECT competition, home, away, date FROM matches GROUP BY "
        find_duplicates_statement += "competition, home, away, date HAVING COUNT(*) > 1;"
        
        self.execute(find_duplicates_statement, commit=False)

        for match in self.cursor.fetchall():

            statement = "SELECT odds_1, odds_x, odds_2, site FROM matches WHERE "
            statement += "competition ='" + match['competition']
            statement += "' AND home ='" + match['home']
            statement += "' AND away ='" + match['away']
            statement += "' AND date ='" + str(match['date']) + "';"

            self.execute(statement)

            max_odds = {}

            for odds_row in self.cursor.fetchall():
                for col in self.odds_cols:

                    if col not in max_odds or odds_row[col] > max_odds[col]['odds']:
                        max_odds[col] = {'odds': odds_row[col], 'site': [odds_row['site']]}
                    elif odds_row[col] == max_odds[col]['odds']:
                        max_odds[col]['site'].append(odds_row['site'])

            arbitrage_sum = 0

            for col in self.odds_cols:
                arbitrage_sum += 1 / max_odds[col]['odds']

            if arbitrage_sum >= 1 and not debug:
                return

            print("%s: %s - %s, %s" % \
                    (match['competition'], match['home'], match['away'], str(match['date'])))
            
            for col in self.odds_cols:
                print(col + ": " + str(max_odds[col]['odds']) + \
                        " (" + ', '.join(max_odds[col]['site']) + ")")

            print("Arbitrage strength: {:.2f}%\n"
                    .format((1 - arbitrage_sum) * 100))
