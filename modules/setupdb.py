import sqlite3
import os.path
import modules.errors
# Const for right values in dbInfo
VALID_VALUES = ('true', 'false')
# Define func for setup
def setup(dbPath: str = 'data\clicks.db'):
    # Connect to local db
    con = sqlite3.connect(dbPath)
    cur = con.cursor()
    # Create table (if not exists)
    try:
        cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            seconds INTAGER,
            clicks INTAGER,
            cps INTAGER,
            date TEXT
        )
        """)
    except sqlite3.DatabaseError as err:
        raise modules.errors.dbError(err) # Raise system error
    # Close it
    cur.close()
    con.close()