#!/usr/bin/env python3

import pymysql, sys

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


    def execute_statement(self, statement):
        
        self.log.write("%s\n\n" % statement)
        self.cursor.execute(statement)
        self.connection.commit()

    def create_table(self):

        create_table_statement = "CREATE TABLE matches (competition VARCHAR(30), home VARCHAR(20), away VARCHAR(20), date DATE, odds_1 DECIMAL(3,2), odds_x  DECIMAL(3,2), odds_2 DECIMAL(3,2), site VARCHAR(50));"
        self.execute_statement(create_table_statement)

    def match_exists(self, comp, home_team, away_team, sql_date, site):
        
        sql_query = "SELECT * FROM matches WHERE "
        
        sql_query += "competition = '" + comp + "' "
        sql_query += "AND home = '" + home_team + "' "
        sql_query += "AND away ='" + away_team + "' "
        sql_query += "AND site ='" + site + "' "
        sql_query += "AND date ='" + sql_date + "';"

        self.execute_statement(sql_query)

        return self.cursor.fetchone() is not None

    def insert_match(self, comp, home_team, away_team, sql_date, site, odds_list):

        insert_query = "INSERT INTO matches (competition, home, away, date, odds_1, odds_x, odds_2, site) VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (comp, home_team, away_team, sql_date, odds_list[0], odds_list[1], odds_list[2], site)

        self.execute_statement(insert_query)
        print("Added %s: '%s - %s' %s, %s" % (comp, home_team, away_team, sql_date, site))
