import MySQLdb

class MyDB(object):
    _db_connection = None
    _db_cur = None

    def __init__(self):
        self._db_connection = MySQLdb.connect('localhost', 'fc_gimel', '', 'fc_gimel_astra')
        self._db_cur = self._db_connection.cursor()
        print("Connection initialized")

    def query(self, query, params):
        return self._db_cur.execute(query, params)

    def __del__(self):
        self._db_connection.close()

    def num_rows(self):
        return cursor.rowcount

"""
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

"""



