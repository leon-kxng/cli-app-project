# models.py
import sqlite3
from threading import Lock
from datetime import datetime

class UserDatabase:
    def __init__(self, user_db_file='users.db', message_db_file='messages.db'):
        self.user_db_file = user_db_file
        self.message_db_file = message_db_file
        self.user_db_lock = Lock()
        self.message_db_lock = Lock()
        self.create_user_table()
        self.create_message_table()

    def create_user_table(self):
        with self.get_user_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )
            ''')

    def create_message_table(self):
        with self.get_message_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    content TEXT NOT NULL
                )
            ''')

    def insert_user(self, username, password):
        with self.get_user_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))

    def insert_message(self, username, content):
        with self.get_message_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO messages (username, content) VALUES (?, ?)', (username, content))

    def get_password(self, username):
        with self.get_user_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            return result[0] if result else None

    def user_exists(self, username):
        with self.get_user_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT 1 FROM users WHERE username = ?', (username,))
            return cursor.fetchone() is not None

    def get_messages(self):
        with self.get_message_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT username, timestamp, content FROM messages ORDER BY timestamp DESC LIMIT 10')
            return cursor.fetchall()

    def close(self):
        pass  # The connections will be closed automatically when exiting the 'with' blocks

    def get_user_connection(self):
        conn = sqlite3.connect(self.user_db_file)
        conn.row_factory = sqlite3.Row
        return conn

    def get_message_connection(self):
        conn = sqlite3.connect(self.message_db_file)
        conn.row_factory = sqlite3.Row
        return conn
