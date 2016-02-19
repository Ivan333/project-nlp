import sqlite3 as lite
import sys

websiteURLs = ['http://www.time.mk/', 'http://stackoverflow.com/questions/5469140/i-want-to-check-whether-a-primary-key-exists-on-sqlite-table','https://www.sqlite.org/lang_createtable.html']

def writeToDatabase(fileName):


    #read site content and loop
    websiteURLs = []
    for line in open(fileName):
        websiteURLs.append(line)



    con = None

    con = lite.connect('test.db')
    cur = con.cursor()
    #cur.execute("DROP TABLE Website")
    cur.execute("CREATE TABLE IF NOT EXISTS Website(Url TEXT PRIMARY KEY, Body Text)")

    with con:

        for url in websiteURLs:
            cur.execute("INSERT OR IGNORE INTO Website(Url, Body) VALUES(?,?);", (url,''))
        con.commit();

        cur.execute("SELECT * FROM Website ")

        rows = cur.fetchall()

        for row in rows:
            print row
    con.close()

writeToDatabase('domeni.txt')
