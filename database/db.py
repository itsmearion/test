import sqlite3

conn = sqlite3.connect("little_nocturne.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT,
    name TEXT,
    description TEXT,
    duration TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    method TEXT
)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    product_id INTEGER,
    payment_method TEXT,
    status TEXT,
    proof TEXT
)
""")
conn.commit()