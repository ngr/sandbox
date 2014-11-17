#!/usr/local/bin/python3.4

import os,string
import MySQLdb
import MyDB 

class word:
    def __init__(self, name):
        self.name = name
    def __doc__(self):
        return "This is a class for words"

    def get_name(self):
        return self.name



print("Running...")

w = word("hello")
print(dir(w))

print(w.__doc__())

print(w.__class__("Bob"))

if __name__ == '__main__':

    print(os.path.abspath(__file__))

print(__name__)


mdb = MyDB.MyDB()
print(mdb)
mdb.query("SHOW TABLES")


