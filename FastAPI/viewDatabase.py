import sqlite3

DATABASE_PATH = 'datenbank.db'

def view_db():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM files')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    conn.close()

if __name__ == "__main__":
    view_db()