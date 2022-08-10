import sqlite3

def connect_db(db):
    # Create a SQL connection SQLite database
    con = sqlite3.connect(db)

    return con.cursor()

def getData(cur):
    # The result of a "cursor.execute" can be iterated over by row
    for row in cur.execute('SELECT * FROM Portfolio;'):
        print(row)

def closeCon():
    # Be sure to close the connection
    con.close()