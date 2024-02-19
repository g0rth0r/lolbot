import sqlite3, os
from contextlib import contextmanager
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

DATABASE_PATH = os.getenv('DATABASE_PATH', 'database/bot.db')

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
        c.execute('''CREATE TABLE IF NOT EXISTS player_config (
    discord_username TEXT PRIMARY KEY,
    bf_username TEXT NOT NULL,
    player_id INTEGER UNIQUE)''')
        c.execute('''CREATE TABLE IF NOT EXISTS player_stats (
    player_id INTEGER,
    stats JSON,  -- SQLite supports storing JSON as text, but you should serialize/deserialize when reading/writing.
    fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(player_id) REFERENCES player_config(player_id))''')
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

# Function to fetch a single player configuration by ID
def fetch_player_config_by_id(player_id):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM player_config WHERE player_id = ?", (player_id,))
        return cursor.fetchone()

# Function to fetch all player configurations
def fetch_all_player_configs():
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM player_config")
        return cursor.fetchall()

# Function to save player stats
def save_player_stats(player_id, stats):
    with get_db_cursor(commit=True) as cursor:
        # Assuming stats is a JSON-serializable dict
        stats_json = json.dumps(stats)
        cursor.execute("INSERT INTO player_stats (player_id, stats) VALUES (?, ?)", (player_id, stats_json))


def fetch_player_config_by_discord_username(discord_username):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM player_config WHERE discord_username = ?", (discord_username,))
        return cursor.fetchone()


def get_most_recent_player_stats(player_id):
    """Fetches the most recent stats for a given player ID."""
    with sqlite3.connect('database/bot.db') as conn:
        conn.row_factory = sqlite3.Row  # This allows us to access columns by name
        cursor = conn.cursor()

        cursor.execute('''SELECT stats FROM player_stats 
                          WHERE player_id = ? 
                          ORDER BY fetched_at DESC 
                          LIMIT 1''', (player_id,))

        row = cursor.fetchone()
        if row:
            # Assuming stats are stored as a serialized JSON string
            return json.loads(row['stats'])
        else:
            return None