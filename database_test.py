#!/usr/bin/env python3

import pymysql

conn = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             db='teams',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cur = conn.cursor()
hosts = cur.execute("SELECT Host,User FROM user")


