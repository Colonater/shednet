import sqlite3

def get_db_connection():
    conn = sqlite3.connect('shed.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                gamename TEXT NOT NULL,
                release_year INTEGER NOT NULL,
                playerscount INTEGER NOT NULL,
                consoles TEXT NOT NULL,
                location TEXT NOT NULL
            )
        ''')
    conn.close()

if __name__ == '__main__':
    init_db()