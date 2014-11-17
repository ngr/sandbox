#!/usr/local/bin/python3.4
# -*- coding: utf-8 -*-

# import MySQLdb module
import MySQLdb

# connect to MySQL using specified settings (everyone of them are optional)
connection = MySQLdb.connect(host="localhost", port=3306, user="fc_gimel", passwd="", db="fc_gimel_astra", charset="utf8")

# open cursor
cursor = connection.cursor()

# execute MySQL query
# can use full power of [1] Format String
# also parameters are auto escaped by library using mysql_real_escape_string
# or if not supported by MySQL then mysql_escape_string
cursor.execute("SHOW TABLES;"
               )

# display row count 
print("Total Rows: {}".format(cursor.rowcount))

# get description about query, eg. column names, etc.
description = cursor.description

column_string = ""
# join all column names
for column in description:
    column_string+=column[0]+" | "
    print("\n | "+column_string+"\n")

# fetch all rows
query_rows = cursor.fetchall()

# process each row
for row in query_rows:
    value_string = ""
    # join row's values
    for value in row:
        value_string+=value+" | "
        print(" | "+value_string)

# close cursor 
cursor.close()

# can also close connection if done with database
connection.close()




