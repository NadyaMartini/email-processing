import sqlite3
import os

DB_FILE = "orders.db"

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT,
            item TEXT
        )
        """)
        conn.commit()
        conn.close()

def save_order(order_id, item):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO orders (order_id, item) VALUES (?, ?)", (str(order_id), item))
    conn.commit()
    conn.close()
