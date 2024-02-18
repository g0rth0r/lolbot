import sqlite3
from contextlib import contextmanager

DATABASE_PATH = './database/bot.db'

def init_db():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS stream_info (
                        id INTEGER PRIMARY KEY,
                        url TEXT,
                        timestamp TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS lolnight_prob (
                        id INTEGER PRIMARY KEY,
                        user_name TEXT NOT NULL,
                        prob INTEGER NOT NULL,
                        date TEXT NOT NULL,
                        UNIQUE(user_name, date))''')
        conn.commit()

@contextmanager
def get_db_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
    finally:
        conn.close()

@contextmanager
def get_db_cursor(commit=False):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    try:
        yield cursor
        if commit:
            conn.commit()
    finally:
        conn.close()

# Example of a utility function to insert or update lolnight_prob
def upsert_lolnight_prob(user_name, prob, date):
    with get_db_cursor(commit=True) as cursor:
        cursor.execute('''INSERT INTO lolnight_prob (user_name, prob, date) VALUES (?, ?, ?)
                          ON CONFLICT(user_name, date) DO UPDATE SET prob = excluded.prob''',
                       (user_name, prob, date))

# fetch the probability of lolnight happening
def fetch_lolnight_probs(date):
    with get_db_cursor() as cursor:
        cursor.execute('SELECT user_name, prob FROM lolnight_prob WHERE date = ?', (date,))
        return cursor.fetchall()

def fetch_latest_stream_info():
    with get_db_cursor() as cursor:
        cursor.execute('SELECT url, timestamp FROM stream_info ORDER BY timestamp DESC LIMIT 1')
        return cursor.fetchone()

def insert_stream_info(url, timestamp):
    with get_db_cursor(commit=True) as cursor:
        # Only insert new stream info without deleting existing entries
        cursor.execute('INSERT INTO stream_info (url, timestamp) VALUES (?, ?)', (url, timestamp))