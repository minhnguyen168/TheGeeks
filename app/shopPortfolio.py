# import sqlite3
#
# def connect_db(db):
#     # Create a SQL connection SQLite database
#     con = sqlite3.connect(db)
#
#     return con.cursor()
#
# def getData(cur):
#     # The result of a "cursor.execute" can be iterated over by row
#     for row in cur.execute('SELECT * FROM Portfolio;'):
#         print(row)
#
# def closeCon():
#     # Be sure to close the connection
#     con.close()
#
# if "__name__"=="__main__":
#     cur = connect_db('site.db')
#     getData(cur)

from app import db

def show(df):
    print(df['portfolio_id'])

#def get_port_name():
