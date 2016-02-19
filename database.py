#!/usr/bin/env python3

import pymysql, sys, time
from decimal import Decimal
from teams import teams

debug = False

MYSQL_UNKNOWN_DATABASE  = 1049

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

        check_existance_statement = "SHOW TABLES LIKE '%s';" % self.matches_table
        self.execute(check_existance_statement)

        if self.cursor.fetchone() is not None:
            return

        decimals = 2
        precision = decimals + 2

        statement = "CREATE TABLE %s (competition VARCHAR(100), home VARCHAR(100), " % self.matches_table
        statement += "away VARCHAR(100), date DATE, "
        statement += "`%s` DECIMAL(%d,%d), %s TIMESTAMP," % (self.odds_cols[0], precision, decimals, self.timestamp_cols[0])
        statement += "`%s` DECIMAL(%d,%d), %s TIMESTAMP," % (self.odds_cols[1], precision, decimals, self.timestamp_cols[1])
        statement += "`%s` DECIMAL(%d,%d), %s TIMESTAMP," % (self.odds_cols[2], precision, decimals, self.timestamp_cols[2])
        statement += "site VARCHAR(100));"

        self.execute(statement)

    def __init__(self):

        self.log = open('.database_log.txt', 'a')
        
        self.database_name  = "odds_data"
        self.matches_table  = "matches"
        
        self.odds_cols      = ['1', 'X', '2']
        self.timestamp_cols = ["timestamp_" + s for s in self.odds_cols]
        
        self.teams          = teams()

        try:
            self.connect()

        except pymysql.err.InternalError as e:
            if e.args[0] != MYSQL_UNKNOWN_DATABASE:
                raise e

            self.create_database()
            self.connect()

        self.cursor = self.connection.cursor()
        
        self.create_table()

    def execute(self, statement, commit=True):
        
        self.log.write("%s\n\n" % statement)
        self.cursor.execute(statement)

        if commit:
            self.connection.commit()

    def insert_match(self, comp, home_team, away_team, sql_date, site, odds, timestamp):

        insert_query = "INSERT INTO matches (competition, home, away, date, site, "
        
        insert_query += "`%s`, %s, " % (self.odds_cols[0], self.timestamp_cols[0])
        insert_query += "`%s`, %s, " % (self.odds_cols[1], self.timestamp_cols[1])
        insert_query += "`%s`, %s) " % (self.odds_cols[2], self.timestamp_cols[2])
        
        insert_query += "VALUES('%s', '%s', '%s', '%s', '%s', " % (comp, home_team, away_team, sql_date, site)
        insert_query += "'%s', '%s', " % (odds['1'], timestamp)
        insert_query += "'%s', '%s', " % (odds['X'], timestamp)
        insert_query += "'%s', '%s');" % (odds['2'], timestamp)
        
        self.execute(insert_query)
        print("Added %s: '%s - %s' %s, %s" % (comp, home_team, away_team, sql_date, site))

    def update_odds(self, comp, home_team, away_team, sql_date, site, new_odds, old_odds, timestamp):
       
        changed_odds = {}

        for col in self.odds_cols:
            if Decimal(str(new_odds[col])) == old_odds[col]:
                continue
            
            changed_odds[col] = Decimal(str(new_odds[col])) - old_odds[col]

        if not changed_odds:
            return

        print("Updated %s: %s - %s, %s, %s" % (comp, home_team, away_team, sql_date, site))

        pairs = []
        
        for col in changed_odds:
            print("%s: %s -> %s (%s)" % (col, old_odds[col], new_odds[col], changed_odds[col]))
            
            timestamp_col = "timestamp_%s" % col
            pairs.append("`%s`='%s', %s='%s'" % (col, new_odds[col], timestamp_col, timestamp))
        
        print()

        statement = "UPDATE %s SET " % self.matches_table
        statement += ", ".join(pairs)

        statement += " WHERE competition = '" + comp
        statement += "' AND home = '" + home_team
        statement += "' AND away ='" + away_team
        statement += "' AND site ='" + site
        statement += "' AND date ='" + sql_date + "';"

        self.execute(statement)

    def process_match(self, comp, home_team, away_team, sql_date, site, odds):

        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')

        home_team = self.teams.get_synonym(home_team)
        away_team = self.teams.get_synonym(away_team)
        
        sql_query = "SELECT `1`, `X`, `2` FROM matches WHERE "
        sql_query += "home = '" + home_team
        sql_query += "' AND away = '" + away_team
        sql_query += "' AND site = '" + site
        sql_query += "' AND date = '" + sql_date + "';"

        self.execute(sql_query, commit=False)
        
        match = self.cursor.fetchone()

        if match is None:
            self.insert_match(comp, home_team, away_team, sql_date, site, odds, timestamp)
            return
        
        old_odds = {col: match[col] for col in self.odds_cols}
        self.update_odds(comp, home_team, away_team, sql_date, site, odds, old_odds, timestamp)

    def find_arbitrages(self):

        find_duplicates_statement = "SELECT competition, home, away, date FROM matches GROUP BY "
        find_duplicates_statement += "home, away, date HAVING COUNT(*) > 1;"
        
        self.execute(find_duplicates_statement, commit=False)

        for match in self.cursor.fetchall():

            statement = "SELECT `1`, `X`, `2`, site FROM matches WHERE "
            statement += "home = '" + match['home']
            statement += "' AND away = '" + match['away']
            statement += "' AND date = '" + str(match['date']) + "';"

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

            if arbitrage_sum >= 1.02 and not debug:
                continue

            print("%s: %s - %s, %s" % \
                    (match['competition'], match['home'], match['away'], str(match['date'])))
            
            for col in self.odds_cols:
                print(col + ": " + str(max_odds[col]['odds']) + \
                        " (" + ', '.join(max_odds[col]['site']) + ")")

            print("Arbitrage strength: {:.2f}%\n"
                    .format((1 - arbitrage_sum) * 100))
