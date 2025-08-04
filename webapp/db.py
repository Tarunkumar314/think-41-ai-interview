import sqlite3
import os

def get_db_connection():
    db_path = os.path.join(os.path.dirname(__file__), 'ecommerce.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # So we can access columns by name
    return conn
