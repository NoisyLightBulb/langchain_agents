import sqlite3
from langchain.tools import Tool

#create connection to database
conn = sqlite3.connect("db.sqlite")


#query database
def run_sqlite_query(query):
    c = conn.cursor()

    try:
        c.execute(query)
        return c.fetchall()
    #catch errors while accessing sqlite database
    except sqlite3.OperationalError as err:
        return f"The following error occured: {str(err)}"


#create tool
run_query_tool = Tool.from_function(
    name = "run_sqlite_query",
    description = "Run a sqlite query.",
    func = run_sqlite_query
)
