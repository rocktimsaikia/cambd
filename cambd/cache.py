import os
import json
import sqlite3

# Don't alter this. Unless you want to deal with permission issues in other places
CACHED_DATABASE = os.path.expanduser("~") + "/.cambd-cache.db"
con = sqlite3.connect(CACHED_DATABASE)


def cache_create():
    sql_create_query = """ CREATE TABLE IF NOT EXISTS words (
    dictionary TEXT,
    word PRIMARY KEY,
    definitions TEXT
    ); """
    con.execute(sql_create_query)

def is_cached(dictionary: str, word: str):
    cur = con.execute("SELECT definitions FROM words WHERE word = ? AND dictionary = ?", (word,dictionary))
    row = cur.fetchone()
    return json.loads(row[0]) if row else None


def cache_append(dictionary: str, word: str, definitions):
    row = dictionary, word, json.dumps(definitions)
    with con:
        con.execute("INSERT OR REPLACE INTO words VALUES (?, ?, ?)", row)


def cache_clear():
    con.execute(""" DROP TABLE IF EXISTS words """)
