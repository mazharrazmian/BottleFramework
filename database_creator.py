import sqlite3 as lite
import sys
con = lite.connect('data\\comments.dat')


print("CREATING DATABASE ......")
with con:
    cur = con.cursor()
    #DROP TABLE
    cur.execute("DROP TABLE IF EXISTS comments")

    #Create Table
    cur.execute("CREATE TABLE comments(id INTEGER PRIMARY KEY AUTOINCREMENT, comment TEXT, name TEXT)")

con.close()
print("DATABASE CREATED")