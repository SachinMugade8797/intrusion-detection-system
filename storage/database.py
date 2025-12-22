import sqlite3
import os
from config.settings import DB_PATH

class Database:
    """Handles SQLite database operations"""
    
    def __init__(self):
        # Ensure data directory exists
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.create_table()
    
    def create_table(self):
        """Create events table if not exists"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                event_type TEXT NOT NULL,
                value INTEGER NOT NULL
            )
        ''')
        self.conn.commit()
        print("Database initialized")
    
    def insert_event(self, event):
        """Insert event into database"""
        cursor = self.conn.cursor()
        cursor.execute(
            'INSERT INTO events (timestamp, event_type, value) VALUES (?, ?, ?)',
            (event['timestamp'], event['event_type'], event['value'])
        )
        self.conn.commit()
        print(f"Event stored: {event['event_type']} at {event['timestamp']}")
    
    def get_recent_events(self, limit=10):
        """Retrieve recent events"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM events ORDER BY id DESC LIMIT ?', (limit,))
        return cursor.fetchall()
    
    def close(self):
        """Close database connection"""
        self.conn.close()
        print("Database connection closed")