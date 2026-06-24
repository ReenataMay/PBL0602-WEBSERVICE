import sqlite3

def init_db():
    conn = sqlite3.connect("carsweb.db")
    cursor = conn.cursor()
    # Membuat tabel jika belum ada
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            merk TEXT NOT NULL,
            model TEXT NOT NULL,
            tahun INTEGER NOT NULL,
            harga REAL NOT NULL
        )
    """)
    
    # Cek apakah tabel kosong, jika ya, isi data contoh
    cursor.execute("SELECT COUNT(*) FROM cars")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO cars (merk, model, tahun, harga) VALUES ('Toyota', 'Avanza', 2022, 250000000)")
        cursor.execute("INSERT INTO cars (merk, model, tahun, harga) VALUES ('Honda', 'Civic', 2023, 600000000)")
        conn.commit()
        
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database berhasil diinisialisasi!")