#!/usr/bin/env python3

import pymysql

class match_database:

    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='teams',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        self.cursor = self.connection.cursor()

        self.log = open('.database_log.txt', 'a')

    def create_table(self):

        create_table_statement = "create table matches (home VARCHAR(20), away VARCHAR(20), date DATE, odds_1 DECIMAL(3,2), odds_x  DECIMAL(3,2), odds_2 DECIMAL(3,2), site VARCHAR(50));"
       

        self.log.write("Executing statement: '%s'\n" % create_table_statement)
        self.cursor.execute(create_table_statement)
        self.connection.commit()

    def execute_statement(self, statement):
        
        self.log.write("Executing statement: '%s'\n" % statement)
        self.cursor.execute(statement)
        self.connection.commit()

    def fetch_one(self):
        
        self.log.write("fetching one\n")
        return self.cursor.fetchone()
