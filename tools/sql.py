import sqlite3
from langchain.tools import Tool

#create connection to database
conn = sqlite3.connect("db.sqlite")


#query database
def run_sqlite_query(query):
    c = conn.cursor()
    c.execute(query)
    return c.fetchall()
