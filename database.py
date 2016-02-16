#!/usr/bin/env python3

import pymysql, sys
import teams

debug = True

class match_database:

    def connect(self, db_name):
        self.connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db=db_name,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    def __init__(self):

        self.log = open('.database_log.txt', 'a')

        self.database_name = "odds_data"
        self.odds_cols = ['odds_1', 'odds_x', 'odds_2']

        try:
            self.connect(self.database_name)
        except pymysql.err.InternalError:
            db1 = pymysql.connect(host="localhost", user="root")
            cursor = db1.cursor()
            cursor.execute('CREATE DATABASE %s;' % self.database_name)
            db1.commit()
            db1.close()

            self.connect(self.database_name)

        self.cursor = self.connection.cursor()

        try:
            self.create_table()
        except:
            pass


    def execute(self, statement):
        
        self.log.write("%s\n\n" % statement)

        self.cursor.execute(statement)
        self.connection.commit()

    def create_table(self):

        statement = "CREATE TABLE matches (competition VARCHAR(30), home VARCHAR(20), away VARCHAR(20), "
        statement += "date DATE, odds_1 DECIMAL(3,2), odds_x  DECIMAL(3,2), odds_2 DECIMAL(3,2), site VARCHAR(50));"
        
        self.execute(statement)

    def change_to_synonym(self, team):

        if team not in teams.synonyms:
            return team
        else:
            return teams.synonyms[team]

    def match_exists(self, comp, home_team, away_team, sql_date, site):

        home_team = self.change_to_synonym(home_team)
        away_team = self.change_to_synonym(away_team)
        
        sql_query = "SELECT * FROM matches WHERE "
        sql_query += "competition = '" + comp + "' "
        sql_query += "AND home = '" + home_team + "' "
        sql_query += "AND away ='" + away_team + "' "
        sql_query += "AND site ='" + site + "' "
        sql_query += "AND date ='" + sql_date + "';"

        self.execute(sql_query)

        return self.cursor.fetchone() is not None

    def insert_match(self, comp, home_team, away_team, sql_date, site, odds_list):

        home_team = self.change_to_synonym(home_team)
        away_team = self.change_to_synonym(away_team)

        insert_query = "INSERT INTO matches (competition, home, away, date, odds_1, odds_x, odds_2, site) "
        insert_query += "VALUES('%s', '%s', '%s', '%s', " % (comp, home_team, away_team, sql_date)
        insert_query += "'%s', '%s', '%s', '%s');" % (odds_list[0], odds_list[1], odds_list[2], site)
        
        #insert_query += "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (comp, home_team, away_team, sql_date, odds_list[0], odds_list[1], odds_list[2], site)

        self.execute(insert_query)
        print("Added %s: '%s - %s' %s, %s" % (comp, home_team, away_team, sql_date, site))

    def find_arbitrages(self):

        find_duplicates_statement = "SELECT competition, home, away, date FROM matches GROUP BY "
        find_duplicates_statement += "competition, home, away, date HAVING COUNT(*) > 1;"
        self.execute(find_duplicates_statement)

        for match in self.cursor.fetchall():

            statement = "SELECT odds_1, odds_x, odds_2, site FROM matches WHERE "
            statement += "competition ='" + match['competition'] + "' "
            statement += "AND home ='" + match['home'] + "' "
            statement += "AND away ='" + match['away'] + "' "
            statement += "AND date ='" + str(match['date']) + "';"

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

            if debug or arbitrage_sum < 1:

                print("%s: %s - %s, %s" % (match['competition'], match['home'], match['away'], str(match['date'])))
                
                for col in self.odds_cols:

                    print(col + ": " + str(max_odds[col]['odds']) + " (" + ', '.join(max_odds[col]['site']) + ")")

                print("Arbitrage strength: {:.2f}%\n"
                        .format((1 - arbitrage_sum) * 100))
