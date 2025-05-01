import sqlite3

conn = sqlite3.connect("little_nocturne.db") c = conn.cursor()

Tabel produk

c.execute(""" CREATE TABLE IF NOT EXISTS products ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT, options TEXT -- JSON string (e.g. ["1 bulan", "3 bulan"]) ) """)

Tabel metode pembayaran

c.execute(""" CREATE TABLE IF NOT EXISTS payment_methods ( id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, type TEXT NOT NULL,          -- "link" atau "text" content TEXT NOT NULL        -- URL atau informasi rekening ) """)

Tabel transaksi

c.execute(""" CREATE TABLE IF NOT EXISTS transactions ( id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, username TEXT, product_id INTEGER NOT NULL, product_option TEXT, payment_method_id INTEGER NOT NULL, proof_file_id TEXT, status TEXT DEFAULT 'pending', timestamp DATETIME DEFAULT CURRENT_TIMESTAMP ) """)

conn.commit() conn.close()

#Fungsi ambil metode pembayaran

def get_payment_methods(): conn = sqlite3.connect("little_nocturne.db") c = conn.cursor() c.execute("SELECT id, name, type, content FROM payment_methods") methods = c.fetchall() conn.close() return methods

Fungsi tambah metode pembayaran (bisa dipakai admin)

def add_payment_method(name: str, type_: str, content: str): conn = sqlite3.connect("little_nocturne.db") c = conn.cursor() c.execute("INSERT INTO payment_methods (name, type, content) VALUES (?, ?, ?)", (name, type_, content)) conn.commit() conn.close()

